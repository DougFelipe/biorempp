/**
 * Semantic Release Configuration (single source of truth)
 *
 * What this file does:
 *  - Calculates the next version from commit messages (Conventional Commits)
 *  - Generates release notes and updates CHANGELOG.md
 *  - Creates a GitHub Release and attaches Python artifacts from ./dist
 *  - Commits CHANGELOG.md back to the repository
 *
 * Notes:
 *  - We DO NOT publish to npm (this is a Python project). Do not add @semantic-release/npm.
 *  - The GitHub workflow must download build artifacts into ./dist before running semantic-release.
 */

module.exports = {
  // Release channels: main = stable, develop/alpha = pre-release (optional)
  branches: [
    'main',
    {
      name: 'develop',
      prerelease: 'beta',
      channel: 'beta',
    },
    {
      name: 'alpha',
      prerelease: 'alpha',
      channel: 'alpha',
    },
  ],

  plugins: [
    /**
     * 1) Determine release type from commit messages
     * We extend Conventional Commits and add a custom type: "notebook".
     * Examples:
     *   feat: new feature -> minor
     *   fix: bug fix -> patch
     *   notebook: update examples/tutorial notebooks -> patch (custom)
     *   refactor/perf/revert -> patch
     *   docs/test/style -> no release
     *   "BREAKING CHANGE" in body -> major
     */
    [
      '@semantic-release/commit-analyzer',
      {
        preset: 'conventionalcommits',
        releaseRules: [
          { type: 'docs', release: false },
          { type: 'test', release: false },
          { type: 'style', release: false },

          { type: 'refactor', release: 'patch' },
          { type: 'perf', release: 'patch' },
          { type: 'revert', release: 'patch' },
          { type: 'fix', release: 'patch' },

          { type: 'feat', release: 'minor' },

          // ✅ Custom type for notebooks
          { type: 'notebook', release: 'minor' },

          // Major bump on explicit breaking changes
          { breaking: true, release: 'major' },

          // Optional scopes
          { scope: 'deps', type: 'fix', release: 'patch' },
          { scope: 'deps', type: 'feat', release: 'minor' },

          // Security fixes always patch
          { type: 'fix', scope: 'security', release: 'patch' },
        ],
        parserOpts: {
          noteKeywords: ['BREAKING CHANGE', 'BREAKING CHANGES', 'BREAKING'],
        },
      },
    ],

    /**
     * 2) Generate release notes content
     * We add a visible section for "notebook" so changes in notebooks are highlighted.
     */
    [
      '@semantic-release/release-notes-generator',
      {
        preset: 'conventionalcommits',
        presetConfig: {
          types: [
            { type: 'feat',     section: '🚀 Features' },
            { type: 'fix',      section: '🐛 Bug Fixes' },
            { type: 'perf',     section: '⚡ Performance Improvements' },
            { type: 'revert',   section: '⏪ Reverts' },

            { type: 'docs',     section: '📚 Documentation', hidden: false },
            { type: 'style',    section: '💎 Styles', hidden: true },
            { type: 'refactor', section: '📦 Code Refactoring' },
            { type: 'test',     section: '🚨 Tests', hidden: true },
            { type: 'build',    section: '🛠 Build System', hidden: true },
            { type: 'ci',       section: '⚙️ Continuous Integration', hidden: true },
            { type: 'chore',    section: '🔧 Maintenance', hidden: true },
            { type: 'notebook', section: '📓 Notebooks', hidden: false },
          ],
        },

        // Optional: transform to improve links in notes
        writerOpts: {
          transform: (commit, context) => {
            const issues = [];

            // Rename breaking header
            commit.notes.forEach((note) => {
              note.title = '💥 BREAKING CHANGES';
            });

            // Normalize scope
            if (commit.scope === '*') commit.scope = '';

            // Short hash
            if (typeof commit.hash === 'string') {
              commit.shortHash = commit.hash.substring(0, 7);
            }

            // Linkify issue refs (#123) and @users
            if (typeof commit.subject === 'string') {
              let url = context.repository
                ? `${context.host}/${context.owner}/${context.repository}`
                : context.repoUrl;

              if (url) {
                url = `${url}/issues/`;
                commit.subject = commit.subject.replace(/#([0-9]+)/g, (_, issue) => {
                  issues.push(issue);
                  return `[#${issue}](${url}${issue})`;
                });
              }

              if (context.host) {
                commit.subject = commit.subject.replace(
                  /\B@([a-z0-9](?:-?[a-z0-9/])*)/g,
                  (_, username) => {
                    if (username.includes('/')) return `@${username}`;
                    return `[@${username}](${context.host}/${username})`;
                  }
                );
              }
            }

            // Drop duplicated refs already linked above
            commit.references = commit.references.filter(
              (reference) => issues.indexOf(reference.issue) === -1
            );

            return commit;
          },
        },
      },
    ],

    /**
     * 3) Update CHANGELOG.md file
     */
    [
      '@semantic-release/changelog',
      {
        changelogFile: 'CHANGELOG.md',
        changelogTitle:
          '# Changelog\n\nAll notable changes to this project will be documented in this file. See [Conventional Commits](https://conventionalcommits.org) for commit guidelines.',
      },
    ],

    /**
     * 4) Create GitHub Release and attach Python artifacts
     * Make sure your GitHub Actions release job downloaded artifacts into ./dist
     * before running semantic-release, otherwise nothing will be attached.
     * Comments are disabled to avoid template parsing issues and noise.
     */
    [
      '@semantic-release/github',
      {
        assets: [
          { path: 'dist/*.tar.gz', label: 'Python Source Distribution' },
          { path: 'dist/*.whl',    label: 'Python Wheel Distribution' },
        ],
        successComment: false,
        failComment: false,
        failTitle: false,
        labels: false,
        releasedLabels: ['released'],
        addReleases: 'bottom',
      },
    ],

    /**
     * 5) Commit CHANGELOG.md back to the repository
     * We only commit CHANGELOG.md (no npm versioning).
     */
    [
      '@semantic-release/git',
      {
        assets: ['CHANGELOG.md'],
        message:
          'chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}',
      },
    ],
  ],
};

/**
 * Semantic Release Configuration
 * Fonte única de configuração. Não use .releaserc.json nem "release" no package.json.
 */

const releaseConfig = {
  // Branch strategy: main (stable) + canais opcionais (beta/alpha)
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
    // Decide o tipo de release com base nos commits
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
          { type: 'fix', release: 'patch' },
          { type: 'feat', release: 'minor' },
          { type: 'revert', release: 'patch' },
          { breaking: true, release: 'major' },

          // Escopos opcionais
          { scope: 'deps', type: 'fix', release: 'patch' },
          { scope: 'deps', type: 'feat', release: 'minor' },

          // Hotfixes de segurança sempre patch
          { type: 'fix', scope: 'security', release: 'patch' },
        ],
        parserOpts: {
          noteKeywords: ['BREAKING CHANGE', 'BREAKING CHANGES', 'BREAKING'],
        },
      },
    ],

    // Gera release notes
    [
      '@semantic-release/release-notes-generator',
      {
        preset: 'conventionalcommits',
        presetConfig: {
          types: [
            { type: 'feat', section: '🚀 Features' },
            { type: 'fix', section: '🐛 Bug Fixes' },
            { type: 'perf', section: '⚡ Performance Improvements' },
            { type: 'revert', section: '⏪ Reverts' },
            { type: 'docs', section: '📚 Documentation', hidden: false },
            { type: 'style', section: '💎 Styles', hidden: true },
            { type: 'refactor', section: '📦 Code Refactoring' },
            { type: 'test', section: '🚨 Tests', hidden: true },
            { type: 'build', section: '🛠 Build System', hidden: true },
            { type: 'ci', section: '⚙️ Continuous Integration', hidden: true },
            { type: 'chore', section: '🔧 Maintenance', hidden: true },
          ],
        },
        writerOpts: {
          // Transform opcional para melhorar links em notas
          transform: (commit, context) => {
            const issues = [];

            commit.notes.forEach((note) => {
              note.title = '💥 BREAKING CHANGES';
            });

            if (commit.scope === '*') commit.scope = '';

            if (typeof commit.hash === 'string') {
              commit.shortHash = commit.hash.substring(0, 7);
            }

            if (typeof commit.subject === 'string') {
              let url = context.repository
                ? `${context.host}/${context.owner}/${context.repository}`
                : context.repoUrl;
              if (url) {
                url = `${url}/issues/`;
                // Issue URLs
                commit.subject = commit.subject.replace(/#([0-9]+)/g, (_, issue) => {
                  issues.push(issue);
                  return `[#${issue}](${url}${issue})`;
                });
              }
              if (context.host) {
                // User URLs
                commit.subject = commit.subject.replace(
                  /\B@([a-z0-9](?:-?[a-z0-9/])*)/g,
                  (_, username) => {
                    if (username.includes('/')) return `@${username}`;
                    return `[@${username}](${context.host}/${username})`;
                  }
                );
              }
            }

            // Remove refs duplicadas já linkadas acima
            commit.references = commit.references.filter((reference) => {
              return issues.indexOf(reference.issue) === -1;
            });

            return commit;
          },
        },
      },
    ],

    // Atualiza CHANGELOG.md
    [
      '@semantic-release/changelog',
      {
        changelogFile: 'CHANGELOG.md',
        changelogTitle:
          '# Changelog\n\nAll notable changes to this project will be documented in this file. See [Conventional Commits](https://conventionalcommits.org) for commit guidelines.',
      },
    ],

    // Cria GitHub Release e anexa artefatos Python (sem comentários automáticos)
    [
      '@semantic-release/github',
      {
        assets: [
          { path: 'dist/*.tar.gz', label: 'Python Source Distribution' },
          { path: 'dist/*.whl', label: 'Python Wheel Distribution' },
        ],
        successComment: false, // ⬅ desabilita o comentário que causava erro
        failComment: false,
        failTitle: false,
        labels: false,
        releasedLabels: ['released'],
        addReleases: 'bottom',
      },
    ],

    // Commita CHANGELOG.md de volta
    [
      '@semantic-release/git',
      {
        assets: ['CHANGELOG.md'],
        message: 'chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}',
      },
    ],
  ],
};

module.exports = releaseConfig;

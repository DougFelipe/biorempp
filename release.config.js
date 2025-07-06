/**
 * Semantic Release Configuration
 *
 * This file provides advanced configuration options for semantic-release
 * beyond what's available in .releaserc.json
 */

const releaseConfig = {
  branches: [
    'main',
    {
      name: 'develop',
      prerelease: 'beta',
      channel: 'beta'
    },
    {
      name: 'alpha',
      prerelease: 'alpha',
      channel: 'alpha'
    }
  ],

  plugins: [
    // Analyze commits to determine release type
    [
      '@semantic-release/commit-analyzer',
      {
        preset: 'conventionalcommits',
        releaseRules: [
          // Custom release rules
          { type: 'docs', release: false },
          { type: 'test', release: false },
          { type: 'style', release: false },
          { type: 'refactor', release: 'patch' },
          { type: 'perf', release: 'patch' },
          { type: 'fix', release: 'patch' },
          { type: 'feat', release: 'minor' },
          { type: 'revert', release: 'patch' },
          { breaking: true, release: 'major' },

          // Custom scopes for specific release types
          { scope: 'deps', type: 'fix', release: 'patch' },
          { scope: 'deps', type: 'feat', release: 'minor' },

          // Security fixes always trigger patch release
          { type: 'fix', scope: 'security', release: 'patch' },
        ],
        parserOpts: {
          noteKeywords: ['BREAKING CHANGE', 'BREAKING CHANGES', 'BREAKING']
        }
      }
    ],

    // Generate release notes
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
            { type: 'chore', section: '🔧 Maintenance', hidden: true }
          ]
        },
        writerOpts: {
          // Custom commit transform for better release notes
          transform: (commit, context) => {
            const issues = []

            commit.notes.forEach(note => {
              note.title = '💥 BREAKING CHANGES'
            })

            if (commit.scope === '*') {
              commit.scope = ''
            }

            if (typeof commit.hash === 'string') {
              commit.shortHash = commit.hash.substring(0, 7)
            }

            if (typeof commit.subject === 'string') {
              let url = context.repository
                ? `${context.host}/${context.owner}/${context.repository}`
                : context.repoUrl
              if (url) {
                url = `${url}/issues/`
                // Issue URLs
                commit.subject = commit.subject.replace(/#([0-9]+)/g, (_, issue) => {
                  issues.push(issue)
                  return `[#${issue}](${url}${issue})`
                })
              }
              if (context.host) {
                // User URLs
                commit.subject = commit.subject.replace(/\B@([a-z0-9](?:-?[a-z0-9/])*)/g, (_, username) => {
                  if (username.includes('/')) {
                    return `@${username}`
                  }
                  return `[@${username}](${context.host}/${username})`
                })
              }
            }

            // Remove duplicate issues
            commit.references = commit.references.filter(reference => {
              if (issues.indexOf(reference.issue) === -1) {
                return true
              }
              return false
            })

            return commit
          }
        }
      }
    ],

    // Update CHANGELOG.md
    [
      '@semantic-release/changelog',
      {
        changelogFile: 'CHANGELOG.md',
        changelogTitle: '# Changelog\n\nAll notable changes to this project will be documented in this file. See [Conventional Commits](https://conventionalcommits.org) for commit guidelines.'
      }
    ],

    // Create GitHub release
    [
      '@semantic-release/github',
      {
        assets: [
          {
            path: 'dist/*.tar.gz',
            label: 'Python Source Distribution'
          },
          {
            path: 'dist/*.whl',
            label: 'Python Wheel Distribution'
          }
        ],
        successComment: `🎉 This \${issue.pull_request ? 'PR is included' : 'issue has been resolved'} in version \${nextRelease.version} 🎉

The release is available on:
- [GitHub Releases](\${releases.filter(release => !!release.name).map(release => \`[\${release.name}](\${release.url})\`).join('\\n- ')})

Your **\${issue.pull_request ? 'pull request' : 'issue'}** is in **\${nextRelease.gitTag}** 🚀`,
        failComment: false,
        failTitle: false,
        labels: false,
        releasedLabels: ['released'],
        addReleases: 'bottom'
      }
    ],

    // Commit back to repository
    [
      '@semantic-release/git',
      {
        assets: ['CHANGELOG.md', 'package.json'],
        message: 'chore(release): \${nextRelease.version} [skip ci]\\n\\n\${nextRelease.notes}'
      }
    ]
  ]
}

module.exports = releaseConfig

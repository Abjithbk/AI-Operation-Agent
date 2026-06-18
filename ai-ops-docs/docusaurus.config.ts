import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'AI Ops Agent',
  tagline: 'AI-powered observability for your production apps',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://your-docs-url.vercel.app',
  baseUrl: '/',

  organizationName: 'your-github-username',
  projectName: 'ai-ops-agent',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: '/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    colorMode: {
      defaultMode: 'dark',
      respectPrefersColorScheme: false,
    },
    navbar: {
      title: 'AI Ops Agent',
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Docs',
        },
        {
          href: 'https://github.com/your-username/ai-ops-agent',
          label: 'GitHub',
          position: 'right',
        },
        {
          href: 'https://your-vercel-url.vercel.app',
          label: 'Live Demo',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            { label: 'Introduction', to: '/' },
            { label: 'Getting Started', to: '/getting-started' },
            { label: 'Authentication', to: '/authentication' },
          ],
        },
        {
          title: 'API Reference',
          items: [
            { label: 'Logs API', to: '/api-reference/logs' },
            { label: 'Metrics API', to: '/api-reference/metrics' },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/your-username/ai-ops-agent',
            },
            {
              label: 'Live Demo',
              href: 'https://your-vercel-url.vercel.app',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} AI Ops Agent. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
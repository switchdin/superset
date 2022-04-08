import { CategoricalScheme } from '@superset-ui/core';

const schemes = [
  {
    id: 'projectsymphony',
    label: 'Project Symphony Colours',
    colors: [
      '#009877',
      '#00968F',
      '#00A9E0',
      '#41B6E6',
      '#E5E6E5',
    ],
  },
].map(s => new CategoricalScheme(s));

export default schemes;
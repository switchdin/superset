import { CategoricalScheme } from '@superset-ui/core';

const schemes = [
  {
    id: 'jacana',
    label: 'Jacana Colours',
    colors: ['#b8c496', '#D9C796', '#F3643D', '#F68224', '#213E52'],
  },
].map(s => new CategoricalScheme(s));

export default schemes;

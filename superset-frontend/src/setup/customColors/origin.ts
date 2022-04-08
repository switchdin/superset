import { CategoricalScheme } from '@superset-ui/core';

const schemes = [
  {
    id: 'origin',
    label: 'Origin Colors',
    colors: ['#FF373C', '#FA4616', '#FF8133', '#FFB92D', '#D44500'],
  },
].map(s => new CategoricalScheme(s));

export default schemes;

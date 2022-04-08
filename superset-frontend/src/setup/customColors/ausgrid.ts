import { CategoricalScheme } from '@superset-ui/core';

const schemes = [
  {
    id: 'ausgrid',
    label: 'AusGrid Colors',
    colors: ['#73B818', '#69AC40', '#008BC0', '#006095', '#1D9CA6'],
  },
].map(s => new CategoricalScheme(s));

export default schemes;

import { CategoricalScheme } from '@superset-ui/core';

const schemes = [
  {
    id: 'sapn',
    label: 'SAPN Colors',
    colors: ['#284051', '#1F4C71', '#FA7A0A', '#535353', '#1A1614'],
  },
].map(s => new CategoricalScheme(s));

export default schemes;

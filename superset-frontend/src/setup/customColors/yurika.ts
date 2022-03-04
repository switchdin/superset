import { CategoricalScheme } from '@superset-ui/core';

const schemes = [
  {
    id: 'yurika',
    label: 'Yurika Colors',
    colors: ['#5e2590', '#b12d76', '#f03f52', '#F37229', '#a13421'],
  },
].map(s => new CategoricalScheme(s));

export default schemes;

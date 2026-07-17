import js from '"'"'@eslint/js'"'"';

export default [
  {
    ignores: ['"'"'logs/**'"'"', '"'"'node_modules/**'"'"', '"'"'coverage/**'"'"'],
  },
  js.configs.recommended,
  {
    files: ['"'"'src/**/*.js'"'"', '"'"'tests/**/*.js'"'"'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: '"'"'commonjs'"'"',
      globals: {
        console: '"'"'readonly'"'"',
        module: '"'"'readonly'"'"',
        process: '"'"'readonly'"'"',
        require: '"'"'readonly'"'"',
      },
    },
    rules: {
      '"'"'no-unused-vars'"'"': ['"'"'error'"'"', { argsIgnorePattern: '"'"'^_'"'"' }],
    },
  },
];

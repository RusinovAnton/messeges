import { nodeResolve } from "@rollup/plugin-node-resolve";
import terser from "@rollup/plugin-terser";

export default [
  {
    input: "src/js/index.js",
    output: {
      file: "../backend/chat/static/index.js",
      format: "cjs",
      sourcemap: true,
      plugins: [terser()],
    },
    plugins: [nodeResolve({ browser: true })],
  }
];

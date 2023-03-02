import { fileURLToPath, URL } from 'node:url'

import { build, defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],

  // 2023-02-28 AJA : Seems to have no effect...
  //appType: 'custom',

  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },

  build: {
    // Save built files in the Django tree (in 'common')
    outDir: '../common/static/common/vue',

    // Since the output dir is not in this Vue tree, we need to force emptying it on build
    emptyOutDir: true,

    // Don't minify for now so it's easyier to understand what's really happening
    // minify: 'terser',
    minify: false,

    rollupOptions: {
        external:['window', 'vue', 'primevue'],
        // Multiple entries does not work for iife format :-(
        input: 'src/demo_widget.js',

        // Only names so it's easier to refer from Django templates
        output: {
          entryFileNames: '[name].js',
          // file: 'bundle.js',
          format: 'iife',
          //name: 'hw',
          globals: {window:'window', vue:'Vue', primevue:'primevue'},
          // inlineDynamicImports: true,
          // manualChunks: ['vue'],
        },
      },
  },
})

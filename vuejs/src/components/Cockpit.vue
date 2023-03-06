<script setup>
import { onBeforeMount, onMounted, ref, reactive, nextTick, getCurrentInstance } from 'vue'
import axios from 'axios'
import primevue from 'primevue'

import { GridLayout, GridItem } from 'vue3-grid-layout-next'
import Accordion from 'primevue/accordion'
import AccordionTab from 'primevue/accordiontab'
import ContextMenu from 'primevue/contextmenu'

const Button = primevue.button
const Dialog = primevue.dialog
const Tooltip = primevue.tooltip
const InputText = primevue.inputtext

// Directive to get tooltips
const vTooltip = Tooltip

const props = defineProps({
  html_id: { type: String, required: true },
  grid_params: {
    type: Object,
    required: true
  },
  palette: { type: Object, required: true }
})

const currentInstance = getCurrentInstance()
const gridData = reactive({ layout: props.grid_params.init_layout })

const tileFormStructure = ref([{ test1: 'popo1' }])
const tileFormIsOpen = ref(false)

const editable = ref(true)

// ref to the grid component
const gridLayout = ref(null)

// refs to the grid elements
const gridItemRefs = ref([])

// Some elements...
const showHelpDialog = ref(false)
const contextMenu = ref()
const contextMenuItems = ref([
  {
    icon: 'pi pi-pencil',
    label: 'Modifier',
    visible: editable.value,
    command: () => {
      unlocked.value = true
    }
  },
  {
    icon: 'pi pi-sync',
    label: 'Rafraîchir',
    command: () => {
      refresh_all()
    }
  }
])

// When the cockpit is unlocked, the user can add, move, resize and remove tiles (= grid items).
const unlocked = ref(false)

// Used to know if the user has added, moved, resized or removed tiles (= grid items).
// if so, the layout will be sent to the server (for storage)
const touched = ref(false)

// ref to the palette (splitter) panel component
// const palettePanel = ref(null)

let mouseXY = { x: null, y: null }
let DragPos = { x: null, y: null, w: 1, h: 1, i: null, w_class: null, w_params: null }

// This function should be shared among all vue widget...
function getCookie(name) {
  'use strict'
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

// Django CSRF token, used for POST requests
const csrftoken = getCookie('csrftoken')

onBeforeMount(() => {
  //grid_data.layout = props.grid_params.init_layout
})

onMounted(() => {
  document.addEventListener(
    'dragover',
    function (e) {
      mouseXY.x = e.clientX
      mouseXY.y = e.clientY
    },
    false
  )
})

function layoutUpdated() {
  //...
  console.log('layout updated')
}

function refresh_all() {
  const params = new URLSearchParams()
  let layout = []
  params.append('widget_id', props.html_id)
  for (var i = 0; i < gridData.layout.length; i++) {
    let tile = gridData.layout[i]
    layout.push({
      i: tile.i,
      w_class: tile.w_class,
      w_params: tile.w_params
    })
  }
  params.append('layout', JSON.stringify(layout))
  axios.get('.', { params }).then((response) => {
    console.log(response.data)
    for (var i = 0; i < gridData.layout.length; i++) {
      let tile = gridData.layout[i]
      if (response.data.tiles.hasOwnProperty(tile.i)) {
        console.log('i=', tile.i, 'html=', response.data.tiles[tile.i].html)
        tile.content = response.data.tiles[tile.i].html
      }
    }
  })
}

function layoutReady() {
  console.log('layout ready')
  // load widgets contents from server
  refresh_all()
}

function editItem(i) {
  //...
  console.log('Editing tile properties...', i)

  let index = gridData.layout.findIndex((item) => item.i === i)
  let tileData = gridData.layout[index]

  tileData.editing = true
  // Build the form from tile template:
  tileFormStructure.value = {
    i: i,
    index: index,
    form: [
      { id: 'title', label: 'Titre', type: 'string', value: tileData.title },
      { label: 'popo suivant 2 ', type: 'string', value: 'pi' }
    ]
  }

  // Open the dialog form
  tileFormIsOpen.value = true
}

function editItemOk() {
  // Save the data in the tile properties
  // ...
  console.log('Saving !')
  let tileData = gridData.layout[tileFormStructure.value.index]
  for (var i = 0; i < tileFormStructure.value.form.length; i++) {
    let parameter = tileFormStructure.value.form[i]
    console.log('  Value:', parameter.label, parameter.value)
    if (parameter.id === 'title') {
      tileData.title = parameter.value
    }
  }
  tileData.editing = false

  touched.value = true

  // Close the dialog form
  tileFormIsOpen.value = false
}

function editItemCancel() {
  let tileData = gridData.layout[tileFormStructure.value.index]
  tileData.editing = false
  // Close the dialog form
  tileFormIsOpen.value = false
}

function modifiedItem(event) {
  // console.log('modified item => touched: true', event)
  touched.value = true
}

function openContextMenu(event) {
  contextMenu.value.show(event)
}

function openHelpDialog() {
  showHelpDialog.value = true
}

function saveLayout() {
  unlocked.value = false
  showHelpDialog.value = false
  if (touched.value) {
    console.log('Storing layout...')
    // Store layout on server:
    //...
    const params = new URLSearchParams()
    params.append('widget_id', props.html_id)
    params.append('layout', JSON.stringify(gridData.layout))
    axios
      .post('.', params, {
        headers: {
          'X-CSRFToken': csrftoken
        }
      })
      .then(function (response) {
        console.log(response)
      })
  }
  touched.value = false
  refresh_all()
}

function removeItem(val) {
  const index = gridData.layout.map((item) => item.i).indexOf(val)
  gridData.layout.splice(index, 1)
}

function drag(e) {
  // Get the grid boundaries
  let parentRect = document.getElementById('grid-container').getBoundingClientRect()

  // Is the mouse pointer in the grid ?
  let mouseInGrid = false
  if (
    mouseXY.x > parentRect.left &&
    mouseXY.x < parentRect.right &&
    mouseXY.y > parentRect.top &&
    mouseXY.y < parentRect.bottom
  ) {
    mouseInGrid = true
  }

  // Put a temporary item in the layout grid (if not already in it)
  if (mouseInGrid === true && gridData.layout.findIndex((item) => item.i === '__drop__') === -1) {
    gridData.layout.push({
      x: (gridData.layout.length * 2) % (gridLayout.value.colNum || 12),
      y: gridData.layout.length + (gridLayout.value.colNum || 12), // puts it at the bottom
      w: 3,
      h: 1,
      i: '__drop__',
      title: '__dropped__'
    })
  }

  // Get index of temporary dragging element
  let index = gridData.layout.findIndex((item) => item.i === '__drop__')
  if (index !== -1) {
    // ??? Try to hide the 'ghost' grid item ???
    //try {
    //  gridItemRefs.value[gridlayout.value.layout.length].$refs.item.style.display = 'none'
    //} catch {}

    // Get the corresponding component
    let el = gridItemRefs.value[index]
    let new_pos = null
    if (el !== undefined) {
      el.dragging = { top: mouseXY.y - parentRect.top, left: mouseXY.x - parentRect.left }
      el.$.attrs.style.display = 'none'
      new_pos = el.calcXY(mouseXY.y - parentRect.top, mouseXY.x - parentRect.left)
    } else {
      new_pos = { x: 0, y: 0 }
    }

    if (mouseInGrid === true) {
      gridLayout.value.dragEvent('dragstart', '__drop__', new_pos.x, new_pos.y, 1, 3)
      let al = gridData.layout.map((a) => a.i)
      let next_id = index
      while (al.includes(next_id)) {
        next_id++
      }
      console.log(al, next_id)
      DragPos.i = next_id
      DragPos.x = gridData.layout[index].x
      DragPos.y = gridData.layout[index].y
      DragPos.w_class = e.target.attributes.w_class.value
      DragPos.w_params = e.target.attributes.w_params.value
    }
    if (mouseInGrid === false) {
      gridLayout.value.dragEvent('dragend', '__drop__', new_pos.x, new_pos.y, 1, 3)
      gridData.layout = gridData.layout.filter((obj) => obj.i !== '__drop__')
    }
  }
}

function dragend(e) {
  touched.value = true
  // Get the grid boundaries
  let parentRect = document.getElementById('grid-container').getBoundingClientRect()

  // Is the mouse pointer in the grid ?
  let mouseInGrid = false
  if (
    mouseXY.x > parentRect.left &&
    mouseXY.x < parentRect.right &&
    mouseXY.y > parentRect.top &&
    mouseXY.y < parentRect.bottom
  ) {
    mouseInGrid = true
  }

  // Put the item in the layout grid
  if (mouseInGrid === true) {
    gridLayout.value.dragEvent('dragend', '__drop__', DragPos.x, DragPos.y, 1, 3)
    gridData.layout = gridData.layout.filter((obj) => obj.i !== '__drop__')
    gridData.layout = [
      ...gridData.layout,
      reactive({
        x: DragPos.x,
        y: DragPos.y,
        w: 3,
        h: 2,
        i: DragPos.i,
        static: false,
        title: 'Dropped !',
        w_class: DragPos.w_class,
        w_params: DragPos.w_params
      })
    ]
    nextTick(() => {
      currentInstance?.proxy?.$forceUpdate()
      gridLayout.value.dragEvent('dragend', DragPos.i, DragPos.x, DragPos.y, 1, 3)
      let index = gridData.layout.findIndex((item) => item.i === DragPos.i)
      let el = gridItemRefs.value[index]
      console.log(index, el)
    })
  }
}
</script>
<template>
  <div
    style="
      height: 100%;
      display: grid;
      grid-auto-flow: column;
      grid-auto-columns: auto minmax(0, 1fr);
    "
  >
    <div class="cockpit-palette" v-show="unlocked">
      <div>Palette</div>
      <Accordion :activeIndex="0">
        <AccordionTab v-for="category in palette">
          <template #header>
            <div style="width: 100%" v-tooltip="category.help_text">
              {{ category.label }}
            </div>
          </template>
          <div
            v-for="(item, tmpl) in category.items"
            @drag="drag"
            @dragend="dragend"
            class="droppable-element palette-item"
            draggable="true"
            unselectable="on"
            :w_class="tmpl"
            w_params='{"toto":10}'
            v-tooltip="item.help_text"
          >
            <div>
              {{ item.label }}
            </div>
          </div>
        </AccordionTab>
      </Accordion>
      <div style="display: flex; justify-content: space-evenly; padding: 12px">
        <Button
          icon="pi pi-question"
          class="p-button-raised p-button-rounded p-button-lg"
          @click="openHelpDialog"
        />
        <Button icon="pi pi-times" class="p-button-raised p-button-rounded p-button-lg" />
        <Button
          icon="pi pi-check"
          class="p-button-raised p-button-rounded p-button-lg"
          @click="saveLayout"
        />
      </div>
    </div>
    <div id="grid-container" class="grid-container" @click="layoutClick">
      <GridLayout
        ref="gridLayout"
        v-model:layout="gridData.layout"
        v-bind:col-num="grid_params.columns"
        v-bind:row-height="grid_params.rows"
        :is-draggable="unlocked"
        :is-resizable="unlocked"
        :is-mirrored="false"
        :prevent-collision="true"
        :vertical-compact="false"
        v-bind:margin="[grid_params.h_spacing, grid_params.v_spacing]"
        :use-css-transforms="true"
        @layout-updated="layoutUpdated"
        @layout-ready="layoutReady"
        @contextmenu="openContextMenu"
      >
        <GridItem
          v-for="(item, index) in gridData.layout"
          ref="gridItemRefs"
          :x="item.x"
          :y="item.y"
          :w="item.w"
          :h="item.h"
          :i="item.i"
          :w_class="item.w_class"
          :w_params="item.w_params"
          :drag-allow-from="'.title'"
          :key="item.i"
          :class="{ 'add-border': item.title, editing: item.editing }"
          :style="{ display: 'block' }"
          @moved="modifiedItem"
          @resized="modifiedItem"
        >
          <div
            class="frame"
            :class="{
              'with-title': item.title.length,
              unlocked: unlocked,
              'without-title': !item.title.length
            }"
          >
            <div
              class="content"
              :class="{ 'with-title': item.title.length }"
              v-if="!item.title.length"
              v-html="item.content"
            ></div>
            <div class="frame-overlay">
              <div class="title" v-if="item.title.length | unlocked">{{ item.title }}</div>
              <div class="remove" v-if="unlocked">
                <i class="pi pi-pencil" @click="editItem(item.i)"></i>
                <i class="pi pi-trash" @click="removeItem(item.i)"></i>
              </div>
              <div class="window" v-if="item.title.length" v-html="item.content"></div>
            </div>
          </div>
        </GridItem>
        <ContextMenu ref="contextMenu" :model="contextMenuItems" />
      </GridLayout>
      <Dialog
        ref="helpDialog"
        header="Utilisation de l'éditeur de cockpit"
        footer=""
        v-model:visible="showHelpDialog"
      >
        Hello !
        <ul>
          <li>Ajouter une tuile</li>
          <li>Supprimer une tuile</li>
          <li>Déplacer une tuile</li>
          <li>Changer la taille d'une tuile</li>
        </ul>
        <p>
          <b>Note :</b> Vous pouvez garder cette aide ouverte et continuer à travailler<br />(vous
          pouvez la déplacer en cliquant sur le titre)
        </p>
      </Dialog>
      <Dialog
        ref="tileForm"
        v-model:visible="tileFormIsOpen"
        header="Test formulaire"
        modal="true"
        @after-hide="editItemCancel"
      >
        <div v-for="formItem in tileFormStructure.form">
          <label>{{ formItem.label }}</label>
          <InputText v-if="formItem.type == 'string'" type="text" v-model="formItem.value" />
        </div>
        <div>
          <Button
            icon="pi pi-times"
            class="p-button-raised p-button-rounded p-button-lg"
            @click="editItemCancel"
          />
          <Button
            icon="pi pi-check"
            class="p-button-raised p-button-rounded p-button-lg"
            @click="editItemOk"
          />
        </div>
      </Dialog>
      <Dialog>
        <div class="dialog-title"></div>
        <form class="dialog-form">
          <fieldset>
            <legend>Modification du Widget :</legend>
            <label>Titre</label><input v-model="edit_widget_title" />
            <template v-for="entry in form">
              <label>{{ entry.label }}</label>
              <input v-if="entry.type == 'int'" v-model.lazy="entry.value" type="number" />
              <input
                v-else-if="entry.type == 'boolean'"
                v-model.lazy="entry.value"
                type="checkbox"
              />
              <input v-else-if="entry.type == 'color'" v-model.lazy="entry.value" type="color" />
              <select v-else-if="entry.type == 'choice'" v-model.lazy="entry.value">
                <option v-for="choice in entry.choices" :value="choice[0]">
                  {{ choice[1] }}
                </option>
              </select>
              <input v-else="" v-model.lazy="entry.value" />
            </template>
          </fieldset>
        </form>
        <div class="form-buttons-box">
          <button class="dialog-button" @click="itemEditOk(edit_item)">Ok</button>
          <button class="dialog-button" @click="itemEditCancel(edit_item)">Annuler</button>
        </div>
      </Dialog>
    </div>
  </div>
</template>
<style>
.cockpit-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
}

.cockpit-palette {
  height: 100%;
  width: 240px;
  display: grid;
  grid-template-rows: auto 1fr auto;
  border: #ddd 1px solid;
}

.p-accordion .p-accordion-content {
  display: flex;
  padding: 5px;
  flex-direction: row;
  flex-wrap: wrap;
  align-content: flex-start;
  align-items: flex-start;
  justify-content: flex-start;
}

.p-button {
  margin: 10px;
}

.palette-item {
  margin: 5px;
  width: 80px;
  height: 80px;
  border: solid 1px #ddd;
  background-color: #fafafa;
  padding: 10px;
}

.grid-container {
  width: 100%;
  height: 100%;
  flex: auto;
}

.vue-grid-layout {
  background: none;
}

.vue-grid-item {
  touch-action: none;
  /* display: grid;* */
  /* grid-template-columns: minmax(0, 1fr) auto;
    grid-template-rows: max-content auto; */
}

.vue-resizable {
  box-sizing: border-box;
}

.vue-grid-item:not(.vue-grid-placeholder):not(.editing) {
  background: #fff;
}

/*
.vue-grid-item.add-border:not(.vue-grid-placeholder) {
  border: 2px solid #eee;
    border-radius: 5px;
}
*/

.vue-grid-item.editing {
  background-color: lightpink;
}

.vue-grid-item.resizing {
  opacity: 0.9;
}

.vue-grid-item.static {
  background: #aaa;
}

.vue-grid-item .frame {
  width: 100%;
  height: 100%;
}

/*
.vue-grid-item .frame.with-title {
}
*/

.vue-grid-item .content {
  width: 100%;
  height: 100%;
}

.vue-grid-item .content.with-title {
  width: 100%;
  height: 100%;
  margin-top: 20px;
}

.vue-grid-item .frame-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;

  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  grid-template-rows: auto minmax(0, 1fr);
}

.vue-grid-item .frame-overlay.without-title {
  pointer-events: none;
}

.vue-grid-item .frame.editable .frame-overlay {
  pointer-events: initial;
}

.vue-grid-item .frame.editable .frame-overlay {
  border: solid #ddd 1px;
  border-radius: 5px;
}

.vue-grid-item .frame.with-title .frame-overlay {
  border: solid #ddd 1px;
  border-radius: 5px;
}

.vue-grid-item .frame-overlay .window {
  grid-column: 1/3;
}

.vue-grid-item .title {
  grid-row: 1;
  grid-column: 1;
  font-size: 16px;
  text-align: center;
  padding: 4px;
  background: #eee;
  opacity: 40%;
}

.vue-grid-item .frame.with-title .title {
  opacity: 100%;
}

.vue-grid-item .remove {
  grid-row: 1;
  grid-column: 2;
  cursor: pointer;
  padding: 2px;
  background: #eee;
  opacity: 50%;
}

.vue-grid-item .frame.with-title .remove {
  opacity: 100%;
}

.vue-grid-item .remove i {
  margin: 4px;
}

.vue-grid-item .content {
  font-size: 16px;
  grid-row: 2;
  grid-column: 1/3;
  overflow: hidden;
}

.vue-grid-item .no-drag {
  height: 100%;
  width: 100%;
}

.vue-grid-item .minMax {
  font-size: 12px;
}

.vue-grid-item .add {
  cursor: pointer;
}

.vue-draggable-handle {
  position: absolute;
  width: 20px;
  height: 20px;
  top: 0;
  left: 0;
  background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10'><circle cx='5' cy='5' r='5' fill='#999999'/></svg>")
    no-repeat bottom right;
  padding: 0 8px 8px 0;
  background-origin: content-box;
  box-sizing: border-box;
  cursor: pointer;
}

.vue-grid-layout div.grid-menu {
  background: #ddd;
  border: none;
  padding: 10px 2px 2px 2px;
  box-shadow: 0 4px 6px 0 rgba(0, 0, 0, 0.4);
}

.vue-grid-layout div.grid-menu span {
  font-size: 20px;
  padding: 12px;
  font-weight: bold;
  text-align: center;
}

.vue-grid-layout ul.grid-menu {
  background: #eee;
  border: none;
  padding: 0;
  margin: 10px 0 0 0;
}

.vue-grid-layout li.grid-menu-entry {
  cursor: pointer;
  font-size: 20px;
  padding: 12px;
  list-style: none inside;
  display: block;
}

.vue-grid-layout li.grid-menu-entry:hover {
  background: #fff;
}
</style>

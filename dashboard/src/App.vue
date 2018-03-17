<template lang="pug">
  #app
    vk-grid(gutter='medium' divided).main-ui
      .uk-width-large
        h2(style='margin-bottom: 0') IrisCentral
        h5(style='margin-top: 0') by WaggleNet
        hr
        disks-page
      .uk-width-expand(v-vk-margin='')
        status-page
        hr
        camera-page
        hr
        sync-page
</template>

<script>
import Nav from './components/nav'
import DisksPage from './components/disks'
import CameraPage from './components/cameras'
import SyncPage from './components/sync'
import StatusPage from './components/status'
import './assets/uikit.css'
import './assets/uikit-mod.sass'
export default {
  name: 'App',
  components: {
    Nav,
    DisksPage,
    CameraPage,
    SyncPage,
    StatusPage
  }
}
</script>

<style lang="sass">
#app
  font-family: 'Avenir', Helvetica, Arial, sans-serif
  -webkit-font-smoothing: antialiased
  -moz-osx-font-smoothing: grayscale
  color: #2c3e50

.main-ui
  padding: 40px
  margin-left: 0px

.card-title
  margin-bottom: 0

p.status-labels
  margin-top: 0
  .uk-label
    margin-right: 10px

div.page-section
  margin-bottom: 21px
</style>

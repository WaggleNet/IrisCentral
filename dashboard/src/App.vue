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
        hr
        sync-page
</template>

<script>
import Nav from './components/nav'
import DisksPage from './components/disks'
import CameraPage from './components/cameras'
import SyncPage from './components/sync'
import StatusPage from './components/status'
import './uikit.css'
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

// Patching uk-card
.uk-card-body
  padding: 25px

.uk-card-footer
  padding: 15px 20px

.uk-card-title
  margin-bottom: 15px

.uk-button
  margin-right: 15px
  vertical-align: middle
  *
    vertical-align: middle

.uk-margin-small-top
  margin-top: 15px !important

h3.uk-heading-bullet .uk-label
  margin-left: 10px

.card-title
  margin-bottom: 0

p.status-labels
  margin-top: 0
  .uk-label
    margin-right: 10px
</style>

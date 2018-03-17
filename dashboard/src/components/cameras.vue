<template lang="pug">
.page-section
  h3.uk-heading-bullet Cameras
    vk-label(type='primary')
      vk-icon(icon='check')
      span {{running}}/{{total}} Capturing
  .camera-list-group(v-vk-margin='')
    camera-card(v-for='i in cameras' :data='i' :key='i.id')
</template>

<script>
import CameraCard from './camera-card'
import wretch from 'wretch'
import _ from 'lodash'
export default {
  components: {
    CameraCard
  },
  data () {
    return {
      cameras: [],
      loading: true,
      total: 0,
      running: 0
    }
  },
  mounted () {
    this.getCameras()
    setInterval(this.getCameras, 5000)
  },
  methods: {
    getCameras () {
      this.loading = true
      wretch('/api/cameras').get()
        .json(data => {
          this.cameras = data
          this.loading = false
          this.total = data.length
          this.running = _.countBy(data, i => i.status === 'running').true || 0
        })
    }
  }
}
</script>

<style lang="sass">
.camera-list-group
  .uk-card
    display: inline-block
    margin-right: 15px
</style>

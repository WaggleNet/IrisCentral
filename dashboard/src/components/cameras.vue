<template lang="pug">
.page-section
  h3.uk-heading-bullet Cameras
    vk-label(type='success')
      vk-icon(icon='check')
      span 3/4 Capturing
  .camera-list-group(v-vk-margin='')
    camera-card(v-for='i in cameras' :data='i' :key='i.id')
</template>

<script>
import CameraCard from './camera-card'
export default {
  components: {
    CameraCard
  },
  data () {
    return {
      cameras: this.getDummyData()
    }
  },
  methods: {
    getDummyData () {
      return [
        {
          name: 'Test Camera 0',
          id: 'iristestv0',
          url: 'rtsp://raspberrypi.local:8554/',
          type: 'video',
          status: 'terminated'
        },
        {
          name: 'IrisCam v1 500MP VL',
          id: 'iristestv1',
          url: 'rtsp://iris01v.local:8554',
          type: 'video',
          status: 'running'
        }
      ]
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

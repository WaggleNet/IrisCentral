<template lang="pug">
  .page-section(v-vk-margin='')
    h3.uk-heading-bullet Storage Devices
      vk-label(type='warning')
        vk-icon(icon='bell')
        span Low Space
    disk-card(v-for='i in disks' :data='i' :key='i.id')
</template>

<script>
import DiskCard from './disk-card'
import { getReadableFileSizeString } from '../utils/humanreadable'
export default {
  components: {
    DiskCard
  },
  data () {
    let dummy = this.getDummyData()
    dummy.forEach(i => {
      i.free = getReadableFileSizeString(i.free_space)
      i.total = getReadableFileSizeString(i.total_capacity)
      i.limit = getReadableFileSizeString(i.space_limit)
    })
    return {
      disks: dummy
    }
  },
  methods: {
    getDummyData () {
      return [
        {
          id: '/Volumes/iristest01',
          free_space: 1503238553,
          total_capacity: 2362232012,
          space_limit: 0,
          candidate: true,
          status: 'active'
        },
        {
          id: '/Volumes/iristest02',
          free_space: 403238553,
          total_capacity: 2362232012,
          space_limit: 0,
          candidate: false,
          status: 'active'
        },
        {
          id: '/Volumes/iristest03',
          free_space: 124353342,
          total_capacity: 2362232012,
          space_limit: 0,
          candidate: false,
          status: 'ejected'
        }
      ]
    }
  }
}
</script>

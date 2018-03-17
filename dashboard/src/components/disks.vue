<template lang="pug">
  .page-section(v-vk-margin='')
    h3.uk-heading-bullet Storage Devices
      vk-label(type='warning')
        vk-icon(icon='bell')
        span Low Space
    disk-card(
      v-for='i in disks'
      :data='i'
      :key='i.id'
      @eject='ejectDisk(i.id)'
      )
</template>

<script>
import DiskCard from './disk-card'
import { getReadableFileSizeString } from '../utils/humanreadable'
import wretch from 'wretch'
export default {
  components: {
    DiskCard
  },
  data () {
    return {
      disks: [],
      loading: true
    }
  },
  mounted () {
    this.getDisks()
    setInterval(this.getDisks, 2000)
  },
  methods: {
    getDisks () {
      this.loading = true
      wretch('/api/drives').get()
        .json(data => {
          data.forEach(i => {
            i.free = getReadableFileSizeString(i.free_space)
            i.total = getReadableFileSizeString(i.total_capacity)
            i.limit = getReadableFileSizeString(i.space_limit)
          })
          this.disks = data
          this.loading = false
        })
    },
    ejectDisk (id) {
      wretch('/api/eject?id=' + encodeURIComponent(id)).get()
        .json(data => {
          this.getDisks()
        })
    }
  }
}
</script>

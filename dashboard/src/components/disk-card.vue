<template lang="pug">
  vk-card
    vk-card-title.card-title {{data.id}}
    p.status-labels
      vk-label(v-if='data.status=="active"') Active
      vk-label(type='warning' v-if='data.status=="ejected"') Ejected
      vk-label(type='success' v-if='data.candidate') In Use
    span {{data.free}} / {{data.total}}
    progress.disk-space(:value='getFreeRatio(data)' max=100)
    div(slot='footer')
      vk-button(type='text' @click='handleEject')
        vk-icon(icon='sign-out')
        span Eject
      vk-button(type='text' @click='handleChangeLimit')
        vk-icon(icon='bolt')
        span Change limit
</template>

<script>
export default {
  props: ['data'],
  methods: {
    getFreeRatio (data) {
      let r = (data.total_capacity - data.free_space) / data.total_capacity
      return Math.trunc(r * 100)
    },
    handleEject (e) {
      e.preventDefault()
      this.$emit('eject')
    },
    handleChangeLimit (e) {
      e.preventDefault()
      // TODO: Change limit implementation
    }
  }
}
</script>

<style lang="sass">
progress.disk-space
  display: block
  width: 100%
  margin-top: 6px
  height: 5px
  border-radius: 0
  -webkit-appearance: none
  appearance: none
  &[value]::-webkit-progress-bar
    background-color: #fff
  &[value]::-webkit-progress-value
    background-color: rgba(60, 176, 236, 1.0)
</style>

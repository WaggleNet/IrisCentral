<template lang="pug">
.page-section
  h3.uk-heading-bullet Status
    vk-label(type='success')
      vk-icon(icon='check')
      span Running
  vk-grid(gutter='small', matched, margin, divided).status-ui
    .uk-width-3-5
      p Stats goes here
    .uk-width-2-5
      .log-output
        p Log file goes here
</template>

<script>
export default {

}
</script>

<style lang="sass">
.log-output
  height: 160px
  overflow: scroll
  border: 1px solid #f6f6f6
  &::-webkit-scrollbar
    display: none
</style>

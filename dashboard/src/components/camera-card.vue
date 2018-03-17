<template lang="pug">
  vk-card.uk-width-medium
    h4.card-title {{data.name}}
    small {{data.url}}
    p.status-labels(v-if='data.status == "running"')
      vk-label(type='success') Active
    p.status-labels(v-else-if='data.status == "terminated"')
      vk-label(type='danger') Terminated
    p.status-labels(v-else-if='data.status == "pending"')
      vk-label(type='warning') Pending
    p.status-labels(v-else)
      vk-label(type='secondary') Unknown
    div(slot='footer')
      vk-button(type='text')
        vk-icon(icon='play')
        span Preview
      vk-button(type='text')
        vk-icon(icon='trash')
        span Delete
</template>

<script>
export default {
  props: ['data']
}
</script>

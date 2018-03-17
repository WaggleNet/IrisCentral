<template lang="pug">
  div
    h3.uk-heading-bullet Sync
    vk-grid(gutter='large' matched)
      .uk-width-2-5
        vk-card(type='primary')
          vk-card-title Box Login
          form(v-vk-margin='')
            input.uk-input(type='email' placeholder='email')
            input.uk-input(type='password' placeholder='password')
            vk-button Sign In
</template>

<script>
export default {

}
</script>

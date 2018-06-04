<template lang="pug">
  div
    h3.uk-heading-bullet Sync
    vk-grid(gutter='large' matched)
      .uk-width-2-5
        vk-card(type='primary')
          vk-card-title WebDAV Login
          form(v-vk-margin='' v-if='!uploader.enabled')
            input.uk-input(type='text' placeholder='Hostname' v-model='uploader.config.hostname')
            input.uk-input(type='text' placeholder='Username' v-model='uploader.config.username')
            input.uk-input(type='password' placeholder='Password' v-model='uploader.config.password')
            input.uk-input(type='text' placeholder='Uploader Location' v-model='uploader.config.location')
            vk-button(@click='handleSubmit') Sign In
          div(v-else)
            span Logged in!
            vk-button(@click='handleLogout') Sign Out
</template>

<script>
import wretch from 'wretch'
export default {
  data: () => ({
    uploader: {
      config: {
        'hostname': '',
        'username': '',
        'password': '',
        'location': ''
      },
      enabled: true,
      active: true
    },
    loading: false
  }),
  methods: {
    getUploaderStatus () {
      this.loading = true
      wretch('/api/uploader').get()
        .json(data => {
          this.uploader = data
          this.loading = false
          if (data.enabled) setTimeout(this.getUploaderStatus, 10000)
        })
    },
    handleSubmit () {
      wretch('/api/uploader/set')
        .json(this.$data.uploader.config)
        .post()
        .json(this.getUploaderStatus)
    },
    handleLogout () {
      wretch('/api/uploader/disable').get()
        .res(this.getUploaderStatus)
    }
  },
  mounted () {
    this.getUploaderStatus()
  }
}
</script>

<template>
  <div><UrlList></UrlList></div>
</template>

<script>
import UrlList from '@/components/UrlList'
export default {
  middleware: ['auth'],
  components: {
    UrlList,
  },
}
</script>

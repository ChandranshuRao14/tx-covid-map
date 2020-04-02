<template>
  <div>
    <main id="map" class="container-fluid" ref="map">
    </main>
  </div>
</template>

<script>
export default {
  name: 'Map',
  data: () => ({
    map: null
  }),
  mounted() {
    this.map = new window.google.maps.Map(this.$refs["map"], {
      center: {lat: 30.259122, lng: -97.748180},
      zoom: 8,
      minZoom: 6,
      gestureHandling: 'cooperative',
      streetViewControl: false,
      mapTypeControl: false,
      fullscreenControl: false,
      restriction: {
        latLngBounds: {
          north: 50, 
          south: 25, 
          west: -130, 
          east: -70
        }
      }
		})
  }
}
</script>

<style scoped>
  #map {
    height: 90vh;
  }
</style>

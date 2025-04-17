<template>
  <div class="container-custom">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
html, body, #app {
  overflow: hidden;

  margin: 0;
  padding: 0;
}

/* From Uiverse.io by SelfMadeSystem */ 
/*
More comprehensive version at shenanigans.shoghisimon.ca/collection/css-blur-blob-bg/
 */

 .container-custom::after {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 1;
  backdrop-filter: hue-rotate(90deg);
  mask: linear-gradient(45deg, #0000, #000);
  animation: rotaty 5s linear infinite;
  transform-origin: center;
}

.container-custom {
  position: absolute;
  background-image: radial-gradient(
    circle at 50% 50%,
    #0000 0,
    #0000 2px,
    hsl(0 0 4%) 2px
  );
  background-size: 8px 8px;
  width: 100%;
  height: 100%;
}


.container-custom::before {
  content: "";
  position: absolute;
  inset: -8em;
  z-index: -1;
  --f: blur(7em) brightness(5);
  --c: #09f;
  animation:
    blobs-1e28bd3d 150s linear infinite,
    thingy 5s linear infinite;
  background-color: #000;
  background-image: radial-gradient(
      ellipse 66px 50px at 50% 50%,
      #0f0 0%,
      transparent 100%
    ),
    radial-gradient(ellipse 77px 60px at 50% 50%, #0f0 0%, transparent 100%),
    radial-gradient(ellipse 78px 100px at 50% 50%, #0f0 0%, transparent 100%),
    radial-gradient(ellipse 73px 96px at 50% 50%, #0f0 0%, transparent 100%),
    radial-gradient(ellipse 76px 77px at 50% 50%, #0f0 0%, transparent 100%),
    radial-gradient(ellipse 66px 51px at 50% 50%, #0f0 0%, transparent 100%),
    radial-gradient(ellipse 90px 57px at 50% 50%, #0f0 0%, transparent 100%),
    radial-gradient(ellipse 89px 93px at 50% 50%, #0f0 0%, transparent 100%);
  background-size:
    726px 576px,
    1242px 454px,
    876px 1160px,
    691px 873px,
    914px 550px,
    1159px 340px,
    1017px 831px,
    313px 977px;
}

</style>

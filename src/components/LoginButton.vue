<template>
    <button class="codepen-button">
        <span v-if="loading">Connexion...</span>
        <span v-else>{{ text }}</span>
    </button>
</template>
<script>
  import '@/assets/tailwind.css'
  export default {
  props: {
    loading: {
      type: Boolean,
    },
    text: {
      type: String,
    }
  }
}
</script>
<style scoped>
  /* Yoinked from CodePen, but improved the animation
  so that it is smooth among other more minor things */

  .codepen-button {
    display: block;
    cursor: pointer;
    color: white;
    margin: 0 auto;
    position: relative;
    text-decoration: none;
    font-weight: 600;
    border-radius: 12px;
    overflow: hidden;
    padding: 5px;
    isolation: isolate;
  }

  .codepen-button::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 400%;
    height: 100%;
    background: linear-gradient(115deg,#4fcf70,#fad648,#a767e5,#12bcfe,#44ce7b);
    background-size: 25% 100%;
    animation: an-at-keyframe-css-at-rule-that-translates-via-the-transform-property-the-background-by-negative-25-percent-of-its-width-so-that-it-gives-a-nice-border-animation_-We-use-the-translate-property-to-have-a-nice-transition-so-it_s-not-a-jerk-of-a-start-or-stop .75s linear infinite;
    animation-play-state: paused;
    translate: -5% 0%;
    transition: translate 0.25s ease-out;
  }

  .codepen-button:hover::before {
    animation-play-state: running;
    transition-duration: 0.75s;
    translate: 0% 0%;
  }

  @keyframes an-at-keyframe-css-at-rule-that-translates-via-the-transform-property-the-background-by-negative-25-percent-of-its-width-so-that-it-gives-a-nice-border-animation_-We-use-the-translate-property-to-have-a-nice-transition-so-it_s-not-a-jerk-of-a-start-or-stop {
    to {
      transform: translateX(-25%);
    }
  }

  .codepen-button span {
    position: relative;
    display: block;
    padding: 0.5rem 1.75rem;
    font-size: 1.1rem;
    background: #000;
    border-radius: 12px;
    height: 100%;
  }
</style>


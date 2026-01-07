let currentScroll = window.pageYOffset;
let targetScroll = currentScroll;
let isScrolling = false;

window.addEventListener("wheel", (e) => {
  e.preventDefault();

  targetScroll += e.deltaY;
  targetScroll = Math.max(
    0,
    Math.min(targetScroll, document.body.scrollHeight - window.innerHeight)
  );

  if (!isScrolling) smoothScroll();
}, { passive: false });

function smoothScroll() {
  isScrolling = true;
  currentScroll += (targetScroll - currentScroll) * 0.1;
  window.scrollTo(0, currentScroll);

  if (Math.abs(targetScroll - currentScroll) > 0.5) {
    requestAnimationFrame(smoothScroll);
  } else {
    isScrolling = false;
  }
}

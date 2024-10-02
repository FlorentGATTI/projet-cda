import { ref } from 'vue';

export function useSwipe({ onSwipeLeft, onSwipeRight, minSwipeDistance = 60 }) {
  const touchStartX = ref(null);
  const touchEndX = ref(null);

  const startTouch = (e) => {
    touchStartX.value = e.touches[0].clientX;
  };

  const moveTouch = (e) => {
    touchEndX.value = e.touches[0].clientX;
  };

  const endTouch = () => {
    if (!touchStartX.value || !touchEndX.value) return;

    const distance = touchStartX.value - touchEndX.value;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;

    if (isLeftSwipe && onSwipeLeft) {
      onSwipeLeft();
    }
    if (isRightSwipe && onSwipeRight) {
      onSwipeRight();
    }

    touchStartX.value = null;
    touchEndX.value = null;
  };

  return { startTouch, moveTouch, endTouch };
}
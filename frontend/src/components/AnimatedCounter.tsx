import React, { useState, useEffect, useRef } from 'react';

interface AnimatedCounterProps {
  to: number;
  duration?: number; // Duration in milliseconds
  decimals?: number;
  suffix?: string;
}

const AnimatedCounter: React.FC<AnimatedCounterProps> = ({
  to,
  duration = 1000,
  decimals = 0,
  suffix = '',
}) => {
  const [current, setCurrent] = useState(0);
  const start = useRef(0);
  const frameRef = useRef(0);
  const startTimeRef = useRef(0);

  const animate = (time: number) => {
    if (!startTimeRef.current) startTimeRef.current = time;
    const progress = (time - startTimeRef.current) / duration;

    if (progress < 1) {
      const easedProgress = easeOutQuad(progress);
      const nextValue = start.current + (to - start.current) * easedProgress;
      setCurrent(nextValue);
      frameRef.current = requestAnimationFrame(animate);
    } else {
      setCurrent(to);
      cancelAnimationFrame(frameRef.current);
    }
  };

  const easeOutQuad = (t: number) => t * (2 - t);

  useEffect(() => {
    start.current = current; // Set start to current value to animate from current to 'to'
    startTimeRef.current = 0; // Reset start time for new animation
    frameRef.current = requestAnimationFrame(animate);

    return () => cancelAnimationFrame(frameRef.current);
  }, [to, duration, decimals]); // Rerun animation if 'to', 'duration', or 'decimals' changes

  return (
    <span>
      {current.toFixed(decimals)}
      {suffix}
    </span>
  );
};

export default AnimatedCounter;

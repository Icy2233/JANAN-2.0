"""
Animation Manager
Handles UI animations like microphone pulse and status transitions
"""

import logging
from typing import Callable, Optional
from threading import Thread, Event
import time

logger = logging.getLogger(__name__)


class AnimationManager:
    """
    Manages UI animations and transitions
    """
    
    def __init__(self):
        """Initialize animation manager"""
        self.animations = {}
        self.is_running = False
        self.stop_event = Event()
        logger.info("Animation Manager initialized")
    
    def create_pulse_animation(self, callback: Callable, 
                              duration: float = 0.5,
                              iterations: int = -1) -> str:
        """
        Create a pulsing animation
        
        Args:
            callback (Callable): Callback function for animation updates
            duration (float): Duration of one pulse cycle in seconds
            iterations (int): Number of iterations (-1 for infinite)
            
        Returns:
            str: Animation ID
        """
        anim_id = f"pulse_{int(time.time() * 1000)}"
        
        animation = {
            'type': 'pulse',
            'callback': callback,
            'duration': duration,
            'iterations': iterations,
            'elapsed': 0,
            'active': True
        }
        
        self.animations[anim_id] = animation
        logger.info(f"Pulse animation created: {anim_id}")
        
        return anim_id
    
    def create_fade_animation(self, callback: Callable,
                             start_value: float = 0.0,
                             end_value: float = 1.0,
                             duration: float = 1.0) -> str:
        """
        Create a fade animation
        
        Args:
            callback (Callable): Callback function for animation updates
            start_value (float): Starting value
            end_value (float): Ending value
            duration (float): Duration in seconds
            
        Returns:
            str: Animation ID
        """
        anim_id = f"fade_{int(time.time() * 1000)}"
        
        animation = {
            'type': 'fade',
            'callback': callback,
            'start_value': start_value,
            'end_value': end_value,
            'duration': duration,
            'elapsed': 0,
            'active': True
        }
        
        self.animations[anim_id] = animation
        logger.info(f"Fade animation created: {anim_id}")
        
        return anim_id
    
    def create_color_transition(self, callback: Callable,
                               start_color: str,
                               end_color: str,
                               duration: float = 1.0) -> str:
        """
        Create a color transition animation
        
        Args:
            callback (Callable): Callback function for animation updates
            start_color (str): Starting hex color
            end_color (str): Ending hex color
            duration (float): Duration in seconds
            
        Returns:
            str: Animation ID
        """
        anim_id = f"color_transition_{int(time.time() * 1000)}"
        
        animation = {
            'type': 'color_transition',
            'callback': callback,
            'start_color': start_color,
            'end_color': end_color,
            'duration': duration,
            'elapsed': 0,
            'active': True
        }
        
        self.animations[anim_id] = animation
        logger.info(f"Color transition animation created: {anim_id}")
        
        return anim_id
    
    def start(self) -> Thread:
        """
        Start the animation loop
        
        Returns:
            Thread: Animation thread
        """
        if self.is_running:
            logger.warning("Animation loop is already running")
            return None
        
        self.is_running = True
        self.stop_event.clear()
        
        thread = Thread(target=self._animation_loop, daemon=True)
        thread.start()
        
        logger.info("Animation loop started")
        return thread
    
    def _animation_loop(self) -> None:
        """Main animation loop"""
        frame_time = 1.0 / 60.0  # 60 FPS
        
        while self.is_running and not self.stop_event.is_set():
            try:
                # Update all active animations
                inactive_anims = []
                
                for anim_id, anim in self.animations.items():
                    if not anim['active']:
                        inactive_anims.append(anim_id)
                        continue
                    
                    anim['elapsed'] += frame_time
                    
                    if anim['type'] == 'pulse':
                        self._update_pulse(anim)
                    elif anim['type'] == 'fade':
                        self._update_fade(anim)
                    elif anim['type'] == 'color_transition':
                        self._update_color_transition(anim)
                
                # Remove inactive animations
                for anim_id in inactive_anims:
                    del self.animations[anim_id]
                
                time.sleep(frame_time)
            
            except Exception as e:
                logger.error(f"Error in animation loop: {str(e)}")
    
    def _update_pulse(self, anim: dict) -> None:
        """Update pulse animation"""
        progress = (anim['elapsed'] % anim['duration']) / anim['duration']
        
        # Sine wave for smooth pulsing
        import math
        value = 0.5 + 0.5 * math.sin(progress * 2 * math.pi)
        
        try:
            anim['callback'](value)
        except Exception as e:
            logger.error(f"Error in pulse animation callback: {str(e)}")
    
    def _update_fade(self, anim: dict) -> None:
        """Update fade animation"""
        if anim['elapsed'] >= anim['duration']:
            value = anim['end_value']
            anim['active'] = False
        else:
            progress = anim['elapsed'] / anim['duration']
            value = anim['start_value'] + (anim['end_value'] - anim['start_value']) * progress
        
        try:
            anim['callback'](value)
        except Exception as e:
            logger.error(f"Error in fade animation callback: {str(e)}")
    
    def _update_color_transition(self, anim: dict) -> None:
        """Update color transition animation"""
        if anim['elapsed'] >= anim['duration']:
            color = anim['end_color']
            anim['active'] = False
        else:
            progress = anim['elapsed'] / anim['duration']
            color = self._interpolate_colors(
                anim['start_color'],
                anim['end_color'],
                progress
            )
        
        try:
            anim['callback'](color)
        except Exception as e:
            logger.error(f"Error in color transition callback: {str(e)}")
    
    @staticmethod
    def _interpolate_colors(color1: str, color2: str, progress: float) -> str:
        """
        Interpolate between two colors
        
        Args:
            color1 (str): Start hex color
            color2 (str): End hex color
            progress (float): Progress from 0 to 1
            
        Returns:
            str: Interpolated hex color
        """
        # Convert hex to RGB
        r1 = int(color1[1:3], 16)
        g1 = int(color1[3:5], 16)
        b1 = int(color1[5:7], 16)
        
        r2 = int(color2[1:3], 16)
        g2 = int(color2[3:5], 16)
        b2 = int(color2[5:7], 16)
        
        # Interpolate
        r = int(r1 + (r2 - r1) * progress)
        g = int(g1 + (g2 - g1) * progress)
        b = int(b1 + (b2 - b1) * progress)
        
        # Convert back to hex
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def stop_animation(self, anim_id: str) -> None:
        """
        Stop a specific animation
        
        Args:
            anim_id (str): Animation ID
        """
        if anim_id in self.animations:
            self.animations[anim_id]['active'] = False
            logger.info(f"Animation stopped: {anim_id}")
    
    def stop_all(self) -> None:
        """Stop all animations"""
        self.is_running = False
        self.stop_event.set()
        self.animations.clear()
        logger.info("All animations stopped")
    
    def pause_animation(self, anim_id: str) -> None:
        """Pause a specific animation"""
        if anim_id in self.animations:
            self.animations[anim_id]['paused'] = True
    
    def resume_animation(self, anim_id: str) -> None:
        """Resume a specific animation"""
        if anim_id in self.animations:
            self.animations[anim_id]['paused'] = False

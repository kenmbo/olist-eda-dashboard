// src/components/common/ChartCard.tsx
import { useState, useEffect, ReactNode } from 'react';
import { Maximize2, Minimize2 } from 'lucide-react';

interface Props {
  children: ReactNode;
  heightClass?: string; // Allows custom heights (e.g., 'h-[500px]' for the map)
}

export default function ChartCard({ children, heightClass = 'h-96' }: Props) {
  const [isExpanded, setIsExpanded] = useState(false);

  /* This effect artificially triggers a window.resize event 
   * (Plotly's useResizeHandler listens to this window.resize event) */
  useEffect(() => {
    // Wait for the 300ms CSS transition to finish, then tell Plotly to resize
    const timer = setTimeout(() => {
      window.dispatchEvent(new Event('resize'));
    }, 300);
    // Cleanup the timer if the component unmounts quickly
    return () => clearTimeout(timer);
  }, [isExpanded]);


  // The base styling shared by both states
  const baseClasses = "bg-gray-900 rounded-lg shadow-md border border-gray-800 group flex flex-col transition-all duration-300";  
  // Sits inside the grid
  const normalClasses = `relative w-full p-4 ${heightClass} ${baseClasses}`;
  // Floats over the entire screen
  const expandedClasses = `fixed inset-4 z-50 p-6 ${baseClasses}`;

  return (
    <>
      {/* Background Dimmer Overlay (only visible when expanded) */}
      {isExpanded && (
        <div 
          className="fixed inset-0 bg-black/70 backdrop-blur-sm z-40" 
          onClick={() => setIsExpanded(false)} 
        />
      )}

      {/* The Card Container */}
      <div className={isExpanded ? expandedClasses : normalClasses}>
        
        {/* The Toggle Button (Appears on hover) */}
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          // Force the button to be opacity-100 when expanded so it's always visible
          className={`absolute top-4 right-4 z-50 p-2 text-gray-400 hover:text-white bg-gray-800 hover:bg-gray-700 rounded-md transition-opacity duration-200 ${
            isExpanded ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'
          }`}
          aria-label={isExpanded ? "Minimize" : "Maximize"}
        >
          {isExpanded ? <Minimize2 size={18} /> : <Maximize2 size={18} />}
        </button>

        {/* The Chart (Plotly) */}
	{/* Added overflow-hidden to prevent Plotly from spilling during transitions.*/}
        <div className="flex-1 w-full h-full relative overflow-hidden">
          {children}
        </div>
      </div>
    </>
  );
}

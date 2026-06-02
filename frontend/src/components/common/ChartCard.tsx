// src/components/common/ChartCard.tsx
import { useState, ReactNode } from 'react';
import { Maximize2, Minimize2 } from 'lucide-react';

interface Props {
  children: ReactNode;
  heightClass?: string; // Allows custom heights (e.g., 'h-[500px]' for the map)
}

export default function ChartCard({ children, heightClass = 'h-96' }: Props) {
  const [isExpanded, setIsExpanded] = useState(false);

  // The base styling shared by both states
  const baseClasses = "bg-gray-900 rounded-lg shadow-md border border-gray-800 relative group flex flex-col transition-all duration-200";
  
  // Sits inside the grid
  const normalClasses = `w-full p-4 ${heightClass} ${baseClasses}`; 
  
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
          className="absolute top-4 right-4 z-10 p-2 text-gray-500 hover:text-white bg-gray-800/80 hover:bg-gray-700 rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200"
          aria-label={isExpanded ? "Minimize" : "Maximize"}
        >
          {isExpanded ? <Minimize2 size={18} /> : <Maximize2 size={18} />}
        </button>

        {/* The Chart (Plotly) */}
        <div className="flex-1 w-full h-full relative">
          {children}
        </div>
      </div>
    </>
  );
}

import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import Sidebar from './components/common/Sidebar';
import type { TabType } from './components/common/Sidebar';
import OrdersContainer from './features/orders/OrdersContainer.tsx'
import CategoryContainer from './features/categories/CategoryContainer.tsx'
import SellerShippingContainer from './features/sellers/SellerShippingContainer';

function App() {
  // State to track which tab is currently selected
  const [activeTab, setActiveTab] = useState<TabType>('orders');

  return (
    // Flex container to hold the sidebar and main content
    <div className="flex h-screen bg-gray-100 overflow-hidden">
      
      {/* Sidebar Component */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Area - notice the ml-64 to offset the fixed 64-width sidebar */}
      <main className="flex-1 ml-64 overflow-y-auto p-8">
        
        <header className="mb-8 border-b border-gray-200 pb-4">
          <h1 className="text-3xl font-bold text-gray-900 capitalize">
            {/* Make the header dynamically match the tab */}
            {activeTab.replace('-', ' ')} Dashboard
          </h1>
        </header>

        {/* Conditionally render containers based on the active tab */}
        <div className="grid grid-cols-1 gap-8 max-w-7xl">
          {activeTab === 'orders' && <OrdersContainer />}
          {activeTab === 'categories' && <CategoryContainer />}
          {activeTab === 'delivery' && <SellerShippingContainer />}
        </div>
        
      </main>
    </div>
  );
}

export default App;

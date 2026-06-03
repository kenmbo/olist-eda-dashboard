import { useState } from 'react';
import Sidebar from './components/common/Sidebar';
import type { TabType } from './components/common/Sidebar';
import OrdersContainer from './features/orders/OrdersContainer.tsx'
import CategoryContainer from './features/categories/CategoryContainer.tsx'
import SellerShippingContainer from './features/sellers/SellerShippingContainer';
import OrdersHeatmapContainer from './features/orders/OrdersHeatmapContainer';
import OrderCostsContainer from './features/orders/OrderCostsContainer';
import CustomerMapContainer from './features/customers/CustomerMapContainer';

function App() {
  // State to track which tab is currently selected
  const [activeTab, setActiveTab] = useState<TabType>('orders');

  return (
    // Flex container to hold the sidebar and main content
    <div className="flex h-screen bg-gray-100 overflow-hidden">
      
      {/* Sidebar Component */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Area - notice the ml-64 to offset the fixed 64-width sidebar */}
      <main className="flex-1 overflow-y-auto p-8">
        
        <header className="mb-8 border-b border-gray-200 pb-4">
          <h1 className="text-3xl font-bold text-gray-900 capitalize">
            {/* Make the header dynamically match the tab */}
            {activeTab.replace('-', ' ')} Dashboard
          </h1>
        </header>

        {/* Conditionally render containers based on the active tab */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 max-w-7xl w-full">

	{/* =======ORDERS======= */}
	{activeTab === 'orders' && (
            <>
              {/* Top Row: Line Chart gets 8 columns (wider), Map gets 4 columns (narrower) */}
              <div className="col-span-1 lg:col-span-8">
                <OrdersContainer />
              </div>
              
              <div className="col-span-1 lg:col-span-4">
                <CustomerMapContainer />
              </div>
              
              {/* Middle Row: Heatmap spans all 12 columns so the timeline is readable */}
              <div className="col-span-1 lg:col-span-12">
                <OrdersHeatmapContainer />
              </div>
              
              {/* Bottom Row: The OrderCostsContainer handles its own 50/50 split internally, 
                  so we give its parent wrapper the full 12 columns */}
              <div className="col-span-1 lg:col-span-12">
                <OrderCostsContainer />
              </div>
            </>
	)}

          {/* ... rest of your tabs ... */}


	{/* =======CATEGORIES======= */}
	{activeTab === 'categories' && (
             <div className="col-span-1 lg:col-span-12">
		<CategoryContainer />
	     </div>
        )}

	{/* =======DELIVERY======= */}
	{activeTab === 'delivery' && (
             <div className="col-span-1 lg:col-span-12">
		<SellerShippingContainer />
	     </div>
        )}

       {/* =======SELLERS======= */}
       {activeTab === 'sellers' && 
             <div className="col-span-12 text-gray-500">
		Sellers & Leads charts coming soon...
	     </div>
       }

       {/* =======PREDICTIONS======= */}
       {activeTab === 'predictions' && 
	     <div className="text-gray-500">
		Predictions & RFM charts coming soon...
	    </div>
       }

       </div> 
      </main>
    </div>
  );
}

export default App;

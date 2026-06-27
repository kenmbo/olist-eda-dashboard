import { useState } from 'react';
import Sidebar from './components/common/Sidebar';
import type { TabType } from './components/common/Sidebar';
import OrdersContainer from './features/orders/OrdersContainer.tsx'
import CategoryContainer from './features/categories/CategoryContainer.tsx'
import SellerShippingContainer from './features/sellers/SellerShippingContainer';
import OrdersHeatmapContainer from './features/orders/OrdersHeatmapContainer';
import OrderCostsContainer from './features/orders/OrderCostsContainer';
import CustomerMapContainer from './features/customers/CustomerMapContainer';
import CategoryMonthlySalesContainer from './features/categories/CategoryMonthlySalesContainer';
import CategoryWeightsContainer from './features/categories/CategoryWeightsContainer';
import DeliveryTrendContainer from './features/delivery/DeliveryTrendContainer';
import DeliveryStagesContainer from './features/delivery/DeliveryStagesContainer';

function App() {
  // State to track which tab is currently selected
  const [activeTab, setActiveTab] = useState<TabType>('orders');

  return (
    // Flex container to hold the sidebar and main content
    <div className="flex h-screen bg-gray-950 text-white overflow-hidden">
      
      {/* Sidebar Component */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Area */}
      <main className="flex-1 overflow-y-auto p-8">
        
        <header className="mb-2 border-b border-gray-400">
          <h1 className="text-3xl font-bold text-gray-200 capitalize">
            {/* Make the header dynamically match the tab */}
            {activeTab.replace('-', ' ')} Dashboard
          </h1>
        </header>

        {/* Conditionally render containers based on the active tab */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-2 max-w-7xl w-full">

	{/* =======ORDERS======= */}
	{activeTab === 'orders' && (
            <>
              <div className="col-span-1 lg:col-span-6">
                <OrdersContainer />
              </div>

              <div className="col-span-1 lg:col-span-6">
                <OrdersHeatmapContainer />
              </div>
              
              <div className="col-span-1 lg:col-span-12">
                <CustomerMapContainer />
              </div>
              
              <div className="col-span-1 lg:col-span-12">
                <OrderCostsContainer />
              </div>
            </>
	)}

	{/* =======CATEGORIES======= */}

	{activeTab === 'categories' && (
            <>
              <div className="col-span-1 lg:col-span-12">
                <CategoryContainer />
              </div>

              <div className="col-span-1 lg:col-span-12">
                <CategoryMonthlySalesContainer />
              </div>

              {/* The new Boxplot */}
              <div className="col-span-1 lg:col-span-12">
                <CategoryWeightsContainer />
              </div>
            </>
          )}
	{/* =======DELIVERY======= */}
	{activeTab === 'delivery' && (
             <div className="col-span-1 lg:col-span-12">
		<SellerShippingContainer />
	     </div>
	     <div className="col-span-1 lg:col-span-12">
		<DeliveryTrendContainer />
	     </div>
       	     <div className="col-span-1 lg:col-span-12">
		<DeliveryStagesContainer />
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

import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import OrdersContainer from './features/orders/OrdersContainer.tsx'
import CategoryContainer from './features/categories/CategoryContainer.tsx'
import SellerShippingContainer from './features/sellers/SellerShippingContainer';

function App() {
  return (
    // min-h-screen ensures the background covers the whole page
    <div className="min-h-screen bg-gray-100 p-4 md:p-8">
      
      {/* max-w-7xl keeps the dashboard from stretching too wide on massive monitors */}
      <div className="max-w-7xl mx-auto">
        
        {/* Dashboard Header */}
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Olist E-commerce Dashboard
          </h1>
          <p className="text-gray-500 mt-2">
            Real-time insights and analytics
          </p>
        </header>

        {/* Dashboard Grid */}
        <main className="grid grid-cols-1 gap-8">
          <OrdersContainer />
	  <CategoryContainer />
	  <SellerShippingContainer />
          
          {/*  Commentting these widgets for now
              <SalesCategoriesContainer />
              <SellerPerformanceContainer />
	  */}
        </main>

      </div>
    </div>
  );
}

export default App

import { BarChart3, Truck, PackageSearch } from 'lucide-react';

// Define the tabs available in your dashboard
export type TabType = 'orders' | 'categories' | 'delivery';

interface Props {
  activeTab: TabType;
  setActiveTab: (tab: TabType) => void;
}

export default function Sidebar({ activeTab, setActiveTab }: Props) {
  const navItems = [
    { id: 'orders', label: 'Order Analysis', icon: BarChart3 },
    { id: 'categories', label: 'Top Categories', icon: PackageSearch },
    { id: 'delivery', label: 'Delivery & Shipping', icon: Truck },
  ] as const;

  return (
    //<aside className="w-64 bg-gray-900 text-white h-screen fixed left-0 top-0 flex flex-col">
   <aside className="w-64 bg-gray-900 text-white flex-shrink-0 flex flex-col">
      <div className="p-6 border-b border-gray-800">
        <h2 className="text-2xl font-bold tracking-tight">Olist App</h2>
      </div>
      
      <nav className="flex-1 py-6 space-y-2 px-4">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors duration-200 ${
                isActive 
                  ? 'bg-blue-600 text-white' 
                  : 'text-gray-400 hover:bg-gray-800 hover:text-white'
              }`}
            >
              <Icon size={20} />
              <span className="font-medium">{item.label}</span>
            </button>
          );
        })}
      </nav>
    </aside>
  );
}

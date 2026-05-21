interface Props {
  activeTab: TabType;
  setActiveTab: (tab: TabType) => void;
}

export type TabType = 'orders' | 'categories' | 'delivery';

export default function Sidebar({ activeTab, setActiveTab }: Props) {
  const navItems = [
    { id: 'orders', label: 'Order Analysis'},
    { id: 'categories', label: 'Top Categories'},
    { id: 'delivery', label: 'Delivery & Shipping'},
  ] as const;

return (
    <aside>
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

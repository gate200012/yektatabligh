import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

interface Post {
  id: number;
  source: string;
  text?: string;
  language?: string;
  created_at: string;
}

interface Overview {
  total_posts: number;
  sentiments: Record<string, number>;
  recent_posts: Post[];
}

const Card: React.FC<{ title: string; children: React.ReactNode }> = ({ title, children }) => (
  <div className="bg-white shadow rounded p-4">
    <h3 className="font-bold mb-2">{title}</h3>
    {children}
  </div>
);

const App: React.FC = () => {
  const [overview, setOverview] = useState<Overview | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);

  useEffect(() => {
    axios.get(`${API_URL}/dashboard/overview`).then((res) => setOverview(res.data));
    axios.get(`${API_URL}/posts`).then((res) => setPosts(res.data));
  }, []);

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      <header className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">داشبورد تحلیل شبکه‌های اجتماعی</h1>
          <p className="text-sm text-slate-600">نسخه آزمایشی با اتصال توییتر و تلگرام</p>
        </div>
        <span className="text-xs bg-indigo-100 text-indigo-700 px-3 py-1 rounded">MVP</span>
      </header>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card title="تعداد کل پست‌ها">{overview?.total_posts ?? 0}</Card>
        <Card title="احساسات مثبت">{overview?.sentiments?.positive ?? 0}</Card>
        <Card title="احساسات منفی">{overview?.sentiments?.negative ?? 0}</Card>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card title="آخرین پست‌ها">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-right">
                <th>شبکه</th>
                <th>متن</th>
              </tr>
            </thead>
            <tbody>
              {posts.slice(0, 5).map((post) => (
                <tr key={post.id} className="border-t">
                  <td className="py-2">{post.source}</td>
                  <td className="py-2">{post.text?.slice(0, 60)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
        <Card title="پیشنهادات ساده">
          <ul className="list-disc pr-4 text-sm space-y-2">
            <li>پست‌های منفی با تعامل بالا را سریع پاسخ دهید.</li>
            <li>از تب "کانکتورها" برای همگام‌سازی لحظه‌ای استفاده کنید.</li>
            <li>قوانین دسته‌بندی را از بخش "دسته‌ها" تنظیم کنید.</li>
          </ul>
        </Card>
      </section>
    </div>
  );
};

export default App;

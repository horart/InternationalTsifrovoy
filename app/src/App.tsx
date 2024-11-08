import './components/Table'
import EnhancedTable from './components/Table'
import { useEffect, useState } from 'react';

export default function App() {
  function createData(
    id: number,
    name: string,
    calories: number,
    fat: number,
    carbs: number,
    protein: number,
  ): Data {
    let x = {
      id,
      name,
      calories,
      fat,  
      carbs,
      protein,
    }
    return x;
  }
  const [rows, setRows] = useState<Data[]>([]);
  useEffect(() => {
    const fetchData = () => {
      fetch('http://localhost:5000/api').then(res => res.text()).then(resp => {
        console.log(resp);
        setRows([...rows, createData(rows.length, resp, rows.length, rows.length, 12, 100)]);
      });
    };
    const timer = setTimeout(fetchData, 2000);
    
    // очистка интервала
    return () => clearInterval(timer);
  }, [rows]);
  return <><EnhancedTable data={rows}></EnhancedTable><h1>{rows.length}</h1></>
}
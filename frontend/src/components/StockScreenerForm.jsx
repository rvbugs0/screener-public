import React, { useState, useEffect } from 'react';

import 'react-datepicker/dist/react-datepicker.css';
import './StockScreenerForm.css';
import CandlestickChart from './charts/CandlestickChart';
import { SERVER_HOST_PORT } from '../constants';
import Sidebar from './sidebar/Sidebar';


const StockScreenerForm = () => {

  const [stocks, setStocks] = useState([]);

  const [selectedStockImage, setSelectedStockImage] = useState(null);

  const [loading, setLoading] = useState(false); // Loading state
  const [expandedStock, setExpandedStock] = useState(null); // Track the expanded stock







  const handleStockClick = (stock) => {
    setSelectedStockImage(stock.image);
    setExpandedStock(expandedStock === stock.name ? null : stock.name);
  };

  return (
    <div className="app-container">
      <div className="navbar">Screener</div>
      <div className="container">


        <Sidebar loading={loading} setLoading={setLoading} setStocks={setStocks}></Sidebar>
        <div className="result-container">
          <h2>Results</h2>
          {loading ? (
            <p>Loading results...</p>
          ) : (
            <ul>
              {stocks.map((stock) => (
                <li key={stock.name}>
                  <div onClick={() => handleStockClick(stock)}>
                    {stock.name}
                  </div>
                  {expandedStock === stock.name && ( // Conditionally render the image
                    // <img
                    //   src={stock.image}
                    //   alt={stock.name}
                    //   className="stock-image" // Add a class for styling
                    // />
                    <div className='chartDiv'>
                      <br />

                      <CandlestickChart  chartData={stock.chart} earlyShifts={stock.early_shifts} trendShifts={stock.shift_in_trend} swingLows={stock.swing_lows} swingHighs={stock.swing_highs}  trend={stock.trend} highOrLowIndex={stock.high_or_low_index} lastHopeIndex={stock.last_hope}/>
                    </div>

                  )}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};
export default StockScreenerForm;

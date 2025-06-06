import { useState, useEffect } from "react";
import ScripDropdown from "../scrip-dropdown/ScripDropdown";
import StrategyDropdown from "../strategy-dropdown/StrategyDropdown";
import DatePicker from 'react-datepicker';
import { SERVER_HOST_PORT } from "../../constants";

const Sidebar = ({loading,setLoading,setStocks}) => {


    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);
    const [interval, setInterval] = useState('');
    const [scrip, setScrip] = useState('');
    const [strategy, setStrategy] = useState('');
    const [isValidDate, setIsValidDate] = useState(true); // Validation state
    const [formOptions, setFormOptions] = useState({})


    useEffect(() => {

        fetch(SERVER_HOST_PORT + "api/form-options").then((res) => res.json()).then((options) => {
          setFormOptions(options)
    
        })
    
      }, [])

      useEffect(() => {
        // Check if endDate is after startDate whenever dates change
        if (startDate && endDate && endDate < startDate) {
          setIsValidDate(false); // Invalid date range
        } else {
          setIsValidDate(true); // Valid date range
        }
      }, [startDate, endDate]);
    
    
    
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true); // Start loading
    
        const response = await fetch(SERVER_HOST_PORT+'/api/stocks', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ startDate, endDate, interval, scrip, strategy }),
        });
    
        const data = await response.json();
    
        if(data.error){
          alert(data.error)
        }
        else{
          setStocks(data);
        }
        
        setLoading(false); // Stop loading
        // const stock_data = [
        //     {"name": "AAPL", "image": "https://unitedfintech.com/wp-content/uploads/2021/08/Example-of-a-flag-pattern-scaled.jpg"},
        //     {"name": "GOOGL", "image": "https://via.placeholder.com/100?text=GOOGL"},
        //     {"name": "AMZN", "image": "https://via.placeholder.com/100?text=AMZN"},
        //     {"name": "MSFT", "image": "https://via.placeholder.com/100?text=MSFT"},
        //     {"name": "TSLA", "image": "https://via.placeholder.com/100?text=TSLA"},
        //     {"name": "FB", "image": "https://via.placeholder.com/100?text=FB"},
        // ]
    
        // setTimeout(()=>{
        //     setLoading(false); // Stop loading
        //     setStocks(stock_data);
        // },3000)
    
      };
    return (
        <div className="form-container">
            {/* <h2>Stock Screener Form</h2> */}
            <form onSubmit={handleSubmit}>
                <label>Start Date</label>
                <DatePicker
                    selected={startDate}
                    onChange={(date) => setStartDate(date)}
                    placeholderText="Select Start Date"
                />
                {!isValidDate && <p className="error-text">End date must be after start date.</p>}
                <label>End Date</label>
                <DatePicker
                    selected={endDate}
                    onChange={(date) => setEndDate(date)}
                    placeholderText="Select End Date"
                    minDate={startDate} // Prevent selecting date before start date
                />

                <label>Interval</label>
                <select value={interval} onChange={(e) => setInterval(e.target.value)}>
                    <option value="" disabled>
                        Select an option
                    </option>
                    {
                        formOptions?.intervals?.map((i) => (
                            <option value={i}>{i}</option>
                        ))

                    }



                </select>
                <label>Scrip</label>

                <ScripDropdown formOptions={formOptions} scrip={scrip} setScrip={setScrip}></ScripDropdown>
                <label>Strategy</label>
                <StrategyDropdown formOptions={formOptions} strategy={strategy} setStrategy={setStrategy}></StrategyDropdown>
                {formOptions ? (<button type="submit">Submit</button>) : (<></>)}
            </form>
            {loading && <div className="loader"></div>} {/* Loader display */}
        </div>
    )
}

export default Sidebar;
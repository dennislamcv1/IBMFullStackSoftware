import React from 'react';
import './bootstrap.min.css';

class EmotionTable extends React.Component {
    render() {
      return (  
        <div>
         
 {JSON.stringify(this.props.emotions)}         
         <table className="table table-bordered">
            <tbody>
              {
                  this.props.emotions && Object.entries(this.props.emotions).map(function (element,val) {
                  return (
                    <tr key={element}>
                      <td>{element[0]}</td>
                        <td>{element[1]}</td>
                    </tr>
                  );
                 })
              }
           </tbody>
           
          </table>
          </div>
          );
        }
    
}
export default EmotionTable;

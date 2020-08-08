// import React from 'react'

// const Samples = ({ samples }) => {
//   return (
//     <div>
//       <center><h1>Samples List</h1></center>
//       {console.log(samples)}
//       {samples.map((sample) => (
//         <div class="samples">
//           <div class="samples-body">
//             <h5 class="original-track">{sample.original_track}</h5>
//             <h6 class="found-smaples">{sample.samples}</h6>
//           </div>
//         </div>
//       ))}
//     </div>
//   )
// };

// export default Samples

import React from 'react'

const Samples = ({ samples }) => {
  return (
    <div>
      <center><h1>Samples List</h1></center>
      {Object.keys(samples).map((item, i) => (
          <div key={i}>
            {console.log(samples[item])}
          <p>{samples[item].name}</p>
          <p>{samples[item].artists}</p>
          </div>
      ))}
    </div>
  )
};

export default Samples
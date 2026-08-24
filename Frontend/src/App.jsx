import React from 'react'
import Chatbot from './Chatbot'
import {Route, Routes} from 'react-router-dom'
import Upload from './Upload'

const App = () => {
  return (
    <div>
      <Routes>
        <Route path='/chat' element={<Chatbot/>}/>
        <Route path='/upload' element={<Upload/>}/>
      </Routes>
    </div>
  )
}

export default App
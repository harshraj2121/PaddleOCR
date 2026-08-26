import React from 'react'
import Chatbot from './Chatbot'
import {Navigate, Route, Routes} from 'react-router-dom'
import Upload from './Upload'

const App = () => {
  return (
    <div>
      <Routes>
        <Route path='/chat' element={<Chatbot/>}/>
        <Route path='/upload' element={<Upload/>}/>

        <Route path='/' element={<Navigate to="/chat" replace/>}/>
        <Route path='*' element={<Navigate to="/chat" replace/>}/>
      </Routes>
    </div>
  )
}

export default App
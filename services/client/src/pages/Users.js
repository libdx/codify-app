import React, { useState, useEffect } from 'react'
import axios from 'axios'
import UsersList from '../components/UsersList'

import 'bulma/css/bulma.css'

const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/users`

const getUsers = async () => {
  const { data: { payload } } = await axios.get(url)
  return payload
}

const Users = () => {

  const [users, setUsers] = useState([])

  useEffect(() => {
    const getData = async () => {
      const users = await getUsers()
      setUsers([ ...users ])
    }

    getData()
  }, [])

  return (
    <section className="section">
      <div className="container">
        <div className="columns">
          <div className="column is-one-third">
            <br/>
            <h1 className="title is-1 is-1">All Users</h1>
            <hr/><br/>
            <UsersList users={users}/>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Users

// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;







// import React, { Component } from "react";
//   let current_date = new Date().getDate()
//     const todoItems = [
//       {
//         id: 1,
//         time_start: "13:00",
//         time_end: "15:00",
//         date: "2021-01-06",
//         activity: "Going fishing",
//         user_invite: 1,
//         completed: true
//       },
//       {
//         id: 2,
//         time_start: "15:00",
//         time_end: "17:00",
//         date: "2021-01-01",
//         activity: "Doing hunting",
//         user_invite: 1,
//         completed: true
//       },
//       {
//         id: 3,
//         time_start: "16:00",
//         time_end: "18:00",
//         date: "2021-01-08",
//         activity: "Doing tobaggoning",
//         user_invite: 1,
//         completed: false
//       },
//       {
//         id: 4,
//         time_start: "17:00",
//         time_end: "19:00",
//         date: "2021-01-09",
//         activity: "Doing excavating",
//         user_invite: 1,
//         completed: false
//       }
//     ];
//     class App extends Component {
//       constructor(props) {
//         super(props);
//         this.state = {
//           viewCompleted: false,
//           todoList: todoItems
//         };
//       }
//       displayCompleted = status => {
//         if (status) {
//           return this.setState({ viewCompleted: true });
//         }
//         return this.setState({ viewCompleted: false });
//       };
//       renderTabList = () => {
//         return (
//           <div className="my-5 tab-list">
//             <span
//               onClick={() => this.displayCompleted(true)}
//               className={this.state.viewCompleted ? "active" : "" 
//             }
//             >
//               complete
//             </span>
//             <span
//               onClick={() => this.displayCompleted(false)}
//               className={this.state.viewCompleted  ? "" : "active"
//             }
//             >
//               Incomplete
//             </span>
//           </div>
//         );
//       };
//       renderItems = () => {
//         const { viewCompleted } = this.state;
//         const newItems = this.state.todoList.filter(
//           item => item.completed == viewCompleted
//         );
//         return newItems.map(item => (
//           <li
//             key={item.id}
//             className="list-group-item d-flex justify-content-between align-items-center"
//           >
//             <span
//               className={`todo-title mr-2 ${
//                 this.state.viewCompleted ? "completed-todo" : ""
//               }`}
//               title={item.activity}
//             >
//               {item.activity}
//             </span>
//             <span>
//               <button className="btn btn-secondary mr-2"> Edit </button>
//               <button className="btn btn-danger">Delete </button>
//             </span>
//           </li>
//         ));
//       };
//       render() {
//         return (
//           <main className="content">
//             <h1 className="text-white text-uppercase text-center my-4">Todo app</h1>
//             <div className="row ">
//               <div className="col-md-6 col-sm-10 mx-auto p-0">
//                 <div className="card p-3">
//                   <div className="">
//                     <button className="btn btn-primary">Add task</button>
//                   </div>
//                   {this.renderTabList()}
//                   <ul className="list-group list-group-flush">
//                     {this.renderItems()}
//                   </ul>
//                 </div>
//               </div>
//             </div>
//           </main>
//         );
//       }
//     }
//     export default App;




import React, { Component } from "react";
    import Modal from "./components/Modal";
    import axios from "axios";

    class App extends Component {
      constructor(props) {
        super(props);
        this.state = {
          viewCompleted: false,
          activeItem: {
            time_start: "",
            time_end: "",
            date: "",
            activity: "",
            user_invite: "",
            completed: false
          },
          todoList: []
        };
      }
      componentDidMount() {
        this.refreshList();
      }
      refreshList = () => {
        axios
          .get("/myapp/allevents")
          .then(res => this.setState({ todoList: res.data }))
          .catch(err => console.log(err));
      };
      displayCompleted = status => {
        if (status) {
          return this.setState({ viewCompleted: true });
        }
        return this.setState({ viewCompleted: false });
      };
      renderTabList = () => {
        return (
          <div className="my-5 tab-list">
            <span
              onClick={() => this.displayCompleted(true)}
              className={this.state.viewCompleted ? "active" : ""}
            >
              complete
            </span>
            <span
              onClick={() => this.displayCompleted(false)}
              className={this.state.viewCompleted ? "" : "active"}
            >
              Incomplete
            </span>
          </div>
        );
      };
      renderItems = () => {
        const { viewCompleted } = this.state;
        const newItems = this.state.todoList.filter(
          item => item.completed === viewCompleted
        );
        
        return newItems.map(item => (
          <li
            key={item.id}
            className="list-group-item d-flex justify-content-between align-items-center"
          >
            <span
              className={`todo-title mr-2 ${
                this.state.viewCompleted ? "completed-todo" : ""
              }`}
              title={item.activity}
            >
              {item.activity}
            </span>
            <span>
              <button
                onClick={() => this.editItem(item)}
                className="btn btn-secondary mr-2"
              >
                {" "}
                Edit{" "}
              </button>
              <button
                onClick={() => this.handleDelete(item)}
                className="btn btn-danger"
              >
                Delete{" "}
              </button>
            </span>
          </li>
        ));
      };
      toggle = () => {
        this.setState({ modal: !this.state.modal });
      };
      handleSubmit = item => {
        this.toggle();
        if (item.id) {
          axios
            .put(`/myapp/allevents/${item.id}/`, item)
            .then(res => this.refreshList());
          return;
        }
        axios
          .post("/myapp/allevents/", item)
          .then(res => this.refreshList());
      };
      handleDelete = item => {
        axios
          .delete(`/myapp/allevents/${item.id}`)
          .then(res => this.refreshList());
      };
      createItem = () => {
        const item = { title: "", description: "", completed: false };
        this.setState({ activeItem: item, modal: !this.state.modal });
      };
      editItem = item => {
        this.setState({ activeItem: item, modal: !this.state.modal });
      };
      render() {
        return (
          <main className="content">
            <h1 className="text-white text-uppercase text-center my-4">Todo app</h1>
            <div className="row ">
              <div className="col-md-6 col-sm-10 mx-auto p-0">
                <div className="card p-3">
                  <div className="">
                    <button onClick={this.createItem} className="btn btn-primary">
                      Add task
                    </button>
                  </div>
                  {this.renderTabList()}
                  <ul className="list-group list-group-flush">
                    {this.renderItems()}
                  </ul>
                </div>
              </div>
            </div>
            {this.state.modal ? (
              <Modal
                activeItem={this.state.activeItem}
                toggle={this.toggle}
                onSave={this.handleSubmit}
              />
            ) : null}
          </main>
        );
      }
    }
    export default App;
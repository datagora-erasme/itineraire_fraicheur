import React, {createContext} from "react"

const MainContext = createContext();

export const MainContextProvider = ({ children }) => {
    const test = "ok context"
    return(
        <MainContext.Provider
            value={{
                test,
            }}
        >
            {children}
        </MainContext.Provider>
    );
};

export default MainContext;
import React from "react";
import { api } from "../api/client";
import type { User } from "../api/types";

export type AuthState = {
	user: User | null;
	loading: boolean;
	login: (email: string, password: string) => Promise<void>;
	register: (email: string, username: string, password: string) => Promise<void>;
	logout: () => void;
};

const AuthContext = React.createContext<AuthState | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
	const [user, setUser] = React.useState<User | null>(null);
	const [loading, setLoading] = React.useState(true);

	React.useEffect(() => {
		(async () => {
			try {
				if (api.getToken()) {
					const me = await api.me();
					setUser(me);
				}
			} catch (e) {
				api.setToken(null);
			} finally {
				setLoading(false);
			}
		})();
	}, []);

	const login = async (email: string, password: string) => {
		await api.login(email, password);
		const me = await api.me();
		setUser(me);
	};

	const register = async (email: string, username: string, password: string) => {
		await api.register(email, username, password);
		await login(email, password);
	};

	const logout = () => {
		api.setToken(null);
		setUser(null);
	};

	return (
		<AuthContext.Provider value={{ user, loading, login, register, logout }}>{children}</AuthContext.Provider>
	);
};

export const useAuth = () => {
	const ctx = React.useContext(AuthContext);
	if (!ctx) throw new Error("useAuth must be used within AuthProvider");
	return ctx;
};

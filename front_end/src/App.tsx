import { DAppProvider, Kovan } from '@usedapp/core';
import React from 'react';
import { Header } from './components';

function App() {
	return (
		<DAppProvider
			config={{
				networks: [Kovan],
				notifications: {
					expirationPeriod: 1000,
					checkInterval: 1000
				}
			}}>
			<Header />
		</DAppProvider>
	);
}

export default App;

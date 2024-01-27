import { createStackNavigator } from '@react-navigation/stack';
import Home from '../views/Home/Home';
import CameraComponent from '../Camera/Camera';

const Stack = createStackNavigator();

export default function HomeStackNavigator() {
    return (
        <Stack.Navigator>
            <Stack.Screen name="Home" component={Home} />
            <Stack.Screen name="Camera" component={CameraComponent} />
        </Stack.Navigator>
    );
}
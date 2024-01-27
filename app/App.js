import 'react-native-gesture-handler';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createMaterialBottomTabNavigator } from '@react-navigation/material-bottom-tabs';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import HomeStackNavigator from './components/StackNavigator/StackNavigator';
import Page2 from './components/views/Page2/Page2';

const Tab = createMaterialBottomTabNavigator();

export default function App() {
  return (
   <NavigationContainer>
       <Tab.Navigator>
        <Tab.Screen name="HomeTab" options={{
          tabBarLabel: 'Home', tabBarIcon: ({ color }) => (
            <MaterialCommunityIcons name="home" color={color} size={26} />
          ),
        }}
          component={HomeStackNavigator} />
           <Tab.Screen
          options={{
            tabBarLabel: 'Updates', tabBarIcon: ({ color }) => (
              <MaterialCommunityIcons name="update" color={color} size={26} />
            ),
          }}
          name="Settings"
          component={Page2} />
      </Tab.Navigator>
      <StatusBar style="auto" />
   </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

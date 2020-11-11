namespace NotificationDispatcher
{
    public static class DispatcherConstants
    {

        /// <summary>
        /// These are the tags the app will send to. These could be subjects like
        /// news, sports, and weather, or they can be custom tags that identify a user
        /// across devices.
        /// </summary>
        public static string[] SubscriptionTags { get; set; } = { "default" };


        /// <summary>
        /// This is the name of your Azure Notification Hub, found in your Azure portal.
        /// </summary>
        public static string NotificationHubName { get; set; } = "NotificationHubSample";

        /// <summary>
        /// This is the "DefaultFullSharedAccessSignature" connection string, which is
        /// found in your Azure Notification Hub portal under "Access Policies".
        /// </summary>
        public static string FullAccessConnectionString { get; set; } = "Endpoint=sb://notificationhubsample-123.servicebus.windows.net/;SharedAccessKeyName=DefaultFullSharedAccessSignature;SharedAccessKey=Nnspdn5CTpI5y/nkLuJ0T8qEBzoDsbRrbFJmJx9Aups=";
    }
}
